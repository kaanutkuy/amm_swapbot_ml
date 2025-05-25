pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address from, address to, uint amount) external returns (bool);
    function transfer(address to, uint amount) external returns (bool);
}

contract AMM {
    IERC20 public token0;
    IERC20 public token1;
    uint112 private reserve0;
    uint112 private reserve1;

    event LiquidityAdded(address indexed provider, uint amount0, uint amount1);
    event Swapped(address indexed trader, address tokenIn, uint amountIn, uint amountOut);

    constructor(address _token0, address _token1) {
        token0 = IERC20(_token0);
        token1 = IERC20(_token1);
    }

    function getReserves() external view returns (uint112, uint112) {
        return (reserve0, reserve1);
    }

    function addLiquidity(uint amount0, uint amount1) external {
        require(amount0 > 0 && amount1 > 0, "AMM: INSUFFICIENT_AMOUNT");

        token0.transferFrom(msg.sender, address(this), amount0);
        token1.transferFrom(msg.sender, address(this), amount1);
        
        reserve0 += uint112(amount0);
        reserve1 += uint112(amount1);

        emit LiquidityAdded(msg.sender, amount0, amount1);
    }

    function swap(address tokenIn, uint amountIn) external {
        require(amountIn > 0, "AMM: INSUFFICIENT_INPUT_AMOUNT");
        bool isToken0 = tokenIn == address(token0);
        require(isToken0 || tokenIn == address(token1), "AMM: INVALID_TOKEN");

        (uint112 _reserve0, uint112 _reserve1) = (reserve0, reserve1);
        IERC20 inToken  = isToken0 ? token0 : token1;
        IERC20 outToken = isToken0 ? token1 : token0;
        uint reserveIn  = isToken0 ? _reserve0 : _reserve1;
        uint reserveOut = isToken0 ? _reserve1 : _reserve0;

        // Apply 0.3% fee
        uint amountInWithFee = amountIn * 997 / 1000;
        uint numerator   = amountInWithFee * reserveOut;
        uint denominator = reserveIn + amountInWithFee;
        uint amountOut   = numerator / denominator;

        require(amountOut > 0, "AMM: INSUFFICIENT_OUTPUT_AMOUNT");

        // execute transfers
        inToken.transferFrom(msg.sender, address(this), amountIn);
        outToken.transfer(msg.sender, amountOut);

        // update reserves
        if (isToken0) {
            reserve0 = uint112(reserveIn + amountIn);
            reserve1 = uint112(reserveOut - amountOut);
        } 
        else {
            reserve1 = uint112(reserveIn + amountIn);
            reserve0 = uint112(reserveOut - amountOut);
        }

        emit Swapped(msg.sender, tokenIn, amountIn, amountOut);
    }
}
