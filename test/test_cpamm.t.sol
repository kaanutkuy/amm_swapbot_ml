pragma solidity ^0.8.0;
import "forge-std/Test.sol";
import "../contracts/cpamm.sol";
import "../contracts/TestToken.sol";

contract AMMTest is Test {
    TestToken token0;
    TestToken token1;
    AMM amm;

    function setUp() public {
        token0 = new TestToken("Token0", "T0", 1e24);
        token1 = new TestToken("Token1", "T1", 1e24);
        amm = new AMM(address(token0), address(token1));
        token0.mint(address(this), 1e21);
        token1.mint(address(this), 1e21);
    }

    function testAddLiquidity() public {
        token0.approve(address(amm), 1e20);
        token1.approve(address(amm), 1e20);
        amm.addLiquidity(1e20, 1e20);
        (uint112 r0, uint112 r1) = amm.getReserves();
        assertEq(r0, 1e20);
        assertEq(r1, 1e20);
    }

    function testSwap() public {
        token0.approve(address(amm), 1e20);
        token1.approve(address(amm), 1e20);
        amm.addLiquidity(1e20, 1e20);
        token0.approve(address(amm), 1e19);
        amm.swap(address(token0), 1e19);
        (, uint112 r1After) = amm.getReserves();
        assertGt(r1After, 0);
    }
}
