// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Certification {
    // Define a struct to represent a certificate
    struct Certificate {
        string customer_id;
        string customer_name;
        string energy_source;
        string capacity_generated;
        string powerhouse_id;
        string powerhouse_name;
        string date_of_claim;
        string ipfs_hash;
    }

    // Mapping to store certificates with their IDs
    mapping(string => Certificate) public certificates;

    // Event to emit when a certificate is generated
    event certificateGenerated(string certificate_id);
    
    // Function to generate a certificate
    function generateCertificate(
        string memory _certificate_id,
        string memory _customer_id,
        string memory _customer_name,
        string memory _energy_source,
        string memory _capacity_generated,
        string memory _powerhouse_id,
        string memory _powerhouse_name,
        string memory _date_of_claim,
        string memory _ipfs_hash
    ) public {
        // Check if certificate with the given ID already exists
        require(
            bytes(certificates[_certificate_id].ipfs_hash).length == 0,
            "Certificate with this ID already exists"
        );

        // Create the certificate
        Certificate memory cert = Certificate({
            customer_id: _customer_id,
            customer_name: _customer_name,
            energy_source: _energy_source,
            capacity_generated: _capacity_generated,
            powerhouse_id: _powerhouse_id,
            powerhouse_name: _powerhouse_name,
            date_of_claim: _date_of_claim,
            ipfs_hash: _ipfs_hash
        });

        // Store the certificate in the mapping
        certificates[_certificate_id] = cert;

        
        // Emit an event
        emit certificateGenerated(_certificate_id);
    }

    // Function to get the details of a certificate
    function getCertificate(
    string memory _certificate_id
)
    public
    view
    returns (
        string memory _customer_id,
        string memory _customer_name,
        string memory _energy_source,
        string memory _capacity_generated,
        string memory _powerhouse_id,
        string memory _powerhouse_name,
        string memory _date_of_claim,
        string memory _ipfs_hash
    )
{
    Certificate memory cert = certificates[_certificate_id];
    
    // Check if the certificate with the given ID exists
    require(
        bytes(certificates[_certificate_id].ipfs_hash).length != 0,
        "Certificate with this ID does not exist"
    );

    // Return the values from the certificate
    return (
        cert.customer_id,
        cert.customer_name,
        cert.energy_source,
        cert.capacity_generated,
        cert.powerhouse_id,
        cert.powerhouse_name,
        cert.date_of_claim,
        cert.ipfs_hash
    );
}

    // Function to check if a certificate is verified
    function isVerified(
        string memory _certificate_id
    ) public view returns (bool) {
        // Check if the IPFS hash of the certificate is not empty
        return bytes(certificates[_certificate_id].ipfs_hash).length != 0;
    }
}
