from brownie import MemeContract, accounts


def test_deploy():
    """
    Arrange
    """
    acc = accounts[0]
    """
    Act
    """
    c = MemeContract.deploy({"from": acc})
    v = c.showAll()
    expected = []
    """
    Assert
    """
    assert v == expected


def test_update():
    acc = accounts[0]
    c = MemeContract.deploy({"from": acc})

    c.setFavMeme("PEPE")
    fav_meme = c.getFavMeme()

    assert fav_meme == "PEPE"

