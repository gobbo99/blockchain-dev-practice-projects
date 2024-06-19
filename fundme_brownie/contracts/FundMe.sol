// SPDX-License-Identifier: MIT

pragma solidity 0.6.6 <0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";  // for versions under 0.8

contract FundMe {
    using SafeMathChainlink for uint256; // doesn't allow for the overflow to occur

    mapping(address => uint256) public addressAmountMapping;
    address[] public funders;
    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function fund() payable public {
        uint256 minimumUsd = 5 * 10 ** 18;
        require(getConversionRate(msg.value) >= minimumUsd, "You need to spend more ETH!");
        addressAmountMapping[msg.sender] = msg.value;
        funders.push(msg.sender);
    }

    function withdraw() payable onlyOwner public {
        require(msg.sender == owner);
        msg.sender.transfer(address(this).balance);
        for (uint256 i=0; i<funders.length; i++) {
            address funder = funders[i];
            addressAmountMapping[funder] = 0;
        }
        funders = new address[](0); // specifying array size
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 inUsd = 50;
        uint256 precision = 1 * 10**18;
        uint256 ethUsd = getPrice();  // returns with 18 decimals precision
        return (inUsd * precision * 10**18) / ethUsd;   // because getPrice() adds 10^10 +
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() internal view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);  // non eth pair, ethusd, so 8 decimals precision
    }

    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 usdValue = (ethPrice * ethAmount) / 1000000000000000000;  // 10^18
        return usdValue;
    }
}
