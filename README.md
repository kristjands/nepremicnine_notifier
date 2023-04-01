# Nepremicnine Scraper and notifier

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Copy the `configuration_example.json` file into `configuration.json` and put in your email adresses and a gmail generated API key.
To generate an API key go to account settings, App passwords, add new App, and copy the generated password.
In configuration.json you can change and add pages you want to check. There exist a simple template what it should look like and also in next section there is description of json elements.

Run
Navigate to this directory.
```bash
source venv/bin/activate
python scraper.py
```
run the bash script on the first run only. I suggest you make a cron tab or nssm.exe for creating window service and add a while loop or with timeouts if you want to automate this.

## Configuration
The configuration is json file. The top level is divided into 4 parts:
- `mail`
- `requests` (optional)
- `json` (optional)
- `selenium` (optional)

The `mail` part is general for all the mails that are sent out. It's parameters are all mandatory:
- `from_email`: the Gmail address the email notification should be sent from
- `gmail_api_key`: generated API key or password for this email address 
- `admin_mail` (optional): the mail of the admin - usually the one who is running the script - to this email the error notification will be sent if there will be any. If not filled the `from_email` tag will be used.

Other parts are optional - the ones that will be filled out, the script will execute the scrapping.

All 3 different types of scrapping have some general configuration:
- `key`: this will be used to seperate different queries to nepremicnine (and other sites in the future)
- `default_url`: root url of the page (for instance: "https://www.nepremicnine.net")
- `page_url`: link of the page you want to scrape, on nepremicnine.net that is all filters used for search
- `to_email`: list of all of recipient's email addresses 
- `mail_subject` (optional): the subject of the email. Defaults to: `Scraper changed`

Let's take a look the specifics of each scrapper type.

`requests`:
  - `bs4_block` (optional): can differ between pages, change if needed. Defaults to `div`.
  - `href_parser` (optional): used for finding links to advert, can differ between pages, change if needed. Defaults to `a`.
  - `bs4_attrs` (optional): is used for searching adverts as full blocks:
    - `class` (optional): is used so we can find the right block within the advert. Defaults to `oglas_container`
    - `itemtype` (optional): so it can be more specific. Defaults to `http://schema.org/ListItem`
  - `info_attributes` (optional): is used to find some info of advert. it has 3 tags:
    - `bs4_block` (optional): block in the webpage where we find the info. Defaults to `div`
    - `bs4_attrs`(optional): is same as before and can be empty. Defaults to empty dictionary
    - `bs4_class`(optional): with class name for more specific search. Defaults to `more_info`
  - `summary_attributes` (optional): is used to find some more info of advert. it has 3 tags:
    - `bs4_block` (optional): block in the webpage where we find the info. Defaults to `div`
    - `bs4_attrs` (optional): is same as before and can be empty. Defaults to empty dictionary
    - `bs4_class` (optional): with class name for more specific search. Defaults to `kratek`

`json`:
  - `request_method` (optional): if the request is sent GET or POST. Defaults to `POST`
  - `post_body` (optional): if the request is set to POST, usually some kind of post body is sent (JSON formatted). You should put this body 
  - `url_postfix` (optional): this is used to create a link. It is created with combination of property `default_url`. The property can have macros in it `{:macro}`, which will be replaced with the data from the response.
  - `url_postfix_macros` (optional): Macros you used in the `url_postfix` separated with `,` - just the values. Those values must exists in the JSON response.
  - `info_attributes` (optional): JSON properties which will be parsed as the information in email. If nothing is passed all the values in JSON will will be included
  - `pagination_name` (optional): This is put into the request JSON, where we can limit the number of items in result per request. This can be added as separate JSON element, which name is equal to set value of this parameter. If it is not set and other `pagiation` parameters are set, they will be append in the request itself (without additional element)
  - `pagination_offset` (optional): How many elements we want to skip. This value is for the first request, after it is changed based on how many request were already made. If we want to apply this all must be present `pagination_offset_name`, `pagination_limit`, `pagination_limit_name`
  - `pagination_offset_name` (optional): Name of the JSON field we will append the `pagination_offset`. If we want to apply this all must be present `pagination_offset`, `pagination_limit`, `pagination_limit_name`
  - `pagination_limit` (optional): How many items in result we want to fetch by one request. If we want to apply this all must be present `pagination_offset`, `pagination_offset_name`, `pagination_limit_name`
  - `pagination_limit_name` (optional):  Name of the JSON field we will append the `pagination_limit`. If we want to apply this all must be present `pagination_offset`, `pagination_offset_name`, `pagination_limit`
  - `pagination_response_name` (partially optional): In the response JSON we usually get a value that tells us how many items are there in total. In case that element has different name that `pagination_name` we can set this here otherwise the value from `pagination_name` will be taken.
  - `pagination_count_all_name` (partially optional): The JSON property where we find total number of items in result (so we know how many request we need to make). If it is empty the 
  - `number_of_cycles` (partially optional): In case there is no element in the response for counting all elements, we can set the max number of request we want to make.
  - `result_name`: The name of the JSON response element that holds the items.

## Contributors
- [LukaAndrojna](https://github.com/LukaAndrojna)
- [KristjanDS](https://github.com/kristjands)
- [pr3mar](https://github.com/pr3mar)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Resources:

https://www.nepremicnine.net/

https://realpython.com/python-concurrency/

https://realpython.com/intro-to-python-threading/

