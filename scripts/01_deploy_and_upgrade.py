from scripts.helpful_scripts import get_account,encode_function_data,upgrade
from brownie import network,Box,ProxyAdmin,TransparentUpgradeableProxy,Contract,BoxV2


def main():
    account = get_account()
    print(f"deploying to {network.show_active()}")
    box = Box.deploy({"from":account},publish_source=True)
    

    proxy_admin = ProxyAdmin.deploy({"from":account},publish_source=True)

    #initializer = box.store, 1
    encoded_function_data = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(box.address,proxy_admin.address,encoded_function_data,{"from":account,"gas_limit":1000000},publish_source=True)
    print(f"proxy deployed to proxy {proxy}, you can now upgrade to V2")
    proxy_box = Contract.from_abi("Box",proxy.address,Box.abi)
    tx = proxy_box.store(1,{"from":account})
    tx.wait(1)

    

    box_v2 = BoxV2.deploy({"from":account},publish_source=True)
    upgrade_transaction = upgrade(account,proxy,box_v2.address,proxy_admin_contract=proxy_admin)
    print("proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2",proxy.address,BoxV2.abi)
    tx2=proxy_box.increment({"from":account})
    tx2.wait(1)
    print(proxy_box.retrive())