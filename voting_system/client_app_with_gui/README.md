App with Gui for a user to perform submitting a vote and getting vote results

To run app run 
`
python3 main.py
`

## Dependencies

stone-cli installed from git@github.com:Wojciech34/stone-cli.git

python and necessary libs (Pyqt5)

sncast and correct account imported into file "~/.starknet_accounts/starknet_open_zeppelin_accounts.json"

Edit snfoundry.toml file in order to provide correct url of 
rpc provider (for blockchain interactions)

Before using app make sure that admin deployed smart contract 
with voting logic, admin in responsible for providing token 
and smart contract address