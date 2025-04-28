# Car Scrapper - Erwin Bonto 

A repository containing the scrapper application powered by Selenium, PostgreSQL, and FastAPI

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirement packages.

```bash
pip install -r requirements.txt
```

## Usage
Run once to get the data from the website
```console
python fetch.py
```
Execute to run application
```console
fastapi dev main.py
```
Once the application is running, the following query can be executed on browser as follows
- Get price range of a specific model
```console
127.0.0.1:8000/price-range/?model="ModelName"
```
- Get most selling car based on month
```console
127.0.0.1:8000/most-selling/?month="MonthInteger"
```
- Get least selling car based on month
```console
127.0.0.1:8000/least-selling/?month="MonthInteger"
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)