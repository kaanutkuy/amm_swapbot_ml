pragma solidity ^0.8.0;

// minimal ERC20 token for local testing
contract TestToken {
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint public totalSupply;
    mapping(address => uint) public balanceOf;
    mapping(address => mapping(address => uint)) public allowance;

    constructor(string memory _name, string memory _symbol, uint _initialSupply) {
        name = _name;
        symbol = _symbol;
        _mint(msg.sender, _initialSupply);
    }

    function _mint(address to, uint amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
    }

    function mint(address to, uint amount) external {
        _mint(to, amount);
    }

    function transfer(address to, uint amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "ERC20: Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }

    function approve(address spender, uint amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(address from, address to, uint amount) external returns (bool) {
        require(balanceOf[from] >= amount, "ERC20: Insufficient balance");
        require(allowance[from][msg.sender] >= amount, "ERC20: Insufficient allowance");
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}
