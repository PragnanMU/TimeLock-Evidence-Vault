// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TimeLockEvidence {
    struct Evidence {
        bytes32 ipfsHash;
        uint256 unlockTime;
        address owner;
    }
    
    mapping(bytes32 => Evidence) public evidences;

    event EvidenceStored(bytes32 indexed ipfsHash, uint256 unlockTime, address indexed owner);

    function storeEvidence(bytes32 _ipfsHash, uint256 _unlockTime) public {
        require(evidences[_ipfsHash].owner == address(0), "Evidence already stored");
        
        evidences[_ipfsHash] = Evidence({
            ipfsHash: _ipfsHash,
            unlockTime: _unlockTime,
            owner: msg.sender
        });

        emit EvidenceStored(_ipfsHash, _unlockTime, msg.sender);
    }

    function getEvidence(bytes32 _ipfsHash) public view returns (uint256, address) {
        require(evidences[_ipfsHash].owner != address(0), "Evidence not found");
        return (evidences[_ipfsHash].unlockTime, evidences[_ipfsHash].owner);
    }
}
