// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// contract that holds information about people that bought meme coins, their profit/loss, do they still hold
// information about submitted information is readable off blockchain
// 

contract MemeContract {

    string favMeme;

    struct subjects {
        string nickname;
        int256 percentageProfit;
        bool stillHold;
    }

    subjects[] private subjectList;
    mapping(string => int256)  nameToProfit; 
    mapping(string => bool)  nameToHoldStatus; 

    function addSubject(string memory _name, int256 _percentageProfit, bool _stillHold) public {
        subjectList.push(subjects(_name,  _percentageProfit, _stillHold));
        nameToProfit[_name] = _percentageProfit;
        nameToHoldStatus[_name] = _stillHold;
    }
    function showAll() public view returns(subjects[] memory) {
        return subjectList;
    }
    function showProfit(string memory _name) public view returns (int256) {
        return nameToProfit[_name];
    }
    function showHoldStatus(string memory _name) public view returns (bool) {
        return nameToHoldStatus[_name];
    }
    function setFavMeme(string memory _favMeme) public{
        favMeme = _favMeme;
    }
    function getFavMeme() public view returns (string memory){
        return favMeme;
    }
}