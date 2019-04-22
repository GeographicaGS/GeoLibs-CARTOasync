# GeoLibs-CARTOasync
Asynchronous Python client for CARTO.

## Features

- [x] SQL API
- [ ] Batch API
- [ ] COPY queries
- [ ] Import API
- [ ] Read and write Panda's DataFrames
- [ ] Maps API?
- [ ] Tests


## Installation

```bash
pip install cartoasync
```

## Usage

### SQL API example

```python
from cartoasync import Auth, SQLClient

auth = Auth(username='username', api_key='api_key')
sql_client = SQLClient(auth)
result = await sql_client.send('SELECT 1 AS one;')

print(result)
>>> {
>>>   "rows": [
>>>     {
>>>       "one": 1
>>>     }
>>>   ],
>>>   "time": 0.002,
>>>   "fields": {
>>>     "one": {
>>>       "type": "number"
>>>     }
>>>   },
>>>   "total_rows": 1
>>> }
```

#### SQL API example, step by step

##### 1. Instantiate an `Auth` object:

###### 1.1. CARTO cloud:

```python
auth = Auth(username='username', api_key='api_key')
```

###### 1.2. CARTO OnPremises or cloud organization with an implict user:

```python
auth = Auth(base_url='https://myapp.com/user/username/', api_key='api_key')
```

###### 1.3. CARTO OnPremises or cloud organization without an implicit user:

```python
auth = Auth(base_url='https://myapp.com/', username='username', api_key='api_key')
```

###### 1.4. SSL:

The `Auth` constructor has and `ssl` attribute. You can use it for handle to the library a [Python's SSL context](https://docs.python.org/3/library/ssl.html#ssl-contexts), or set it to `False` for relaxing certification checks. More info on [AIOHTTP doc](https://docs.aiohttp.org/en/stable/client_advanced.html#ssl-control-for-tcp-sockets).

##### 2. Instantiate the SQLClient and send queries:

###### 2.1. SQLClient's own AIOHTTP session:

```python
sql_client = SQLClient(auth)
result = await sql_client.send('SELECT 1 AS one;')
```

###### 2.2. External AIOHTTP session you need to care until the end of its days:

```python
import aiohttp

sql_client = SQLClient(auth)
result = await sql_client.send('SELECT 1 AS one;', aiohttp.ClientSession())
```
