// SPDX-License-Identifier: GPL-3.0

pragma solidity >= 0.5.0 < 0.9.0;

contract SupplyChain {

    mapping(uint256 => Chain[]) public chains;

    struct Chain {
        uint chainId;
        address _addressOfChainMember;
        bool signed;
    }

  struct Product {
    uint256 productId;
    address manufacturer;
    address customer;
    uint64 price;
    string productName;
    string productDescription;
    string[] productImages;
    uint256 dateManufactured;
    uint256 dateReceived;
  }

  mapping(uint256 => Product) public products;
  uint256 public productCount = 10000001; // setting the initial product id to be used

  event ProductManufactured(uint256 productId, address manufacturer);
  event ProductSignedByRetailer(uint256 productId, address retailer);
  event ProductReceived(uint256 productId, address customer);

  function manufactureProduct(string memory _productName, string memory _productDescription, string[] memory _productImages) public {
    productCount++;
    products[productCount] = Product(productCount, msg.sender, address(0), 0, _productName, _productDescription, _productImages, block.timestamp, 0);
    emit ProductManufactured(productCount, msg.sender);
  }


  function getProductDetails(uint256 _productId) public view returns (uint256, uint64, string[] memory, uint256, uint256) {
    return (
      products[_productId].productId,
      products[_productId].price,
      products[_productId].productImages,
      products[_productId].dateManufactured,
      products[_productId].dateReceived
    );
  }

}
