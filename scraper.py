import json
from os import path

from helpers.page import load_configs
from helpers.listings import Listings
from helpers.mail import Mail
from helpers.parsers.parsers import Parsers

def main():
    try:
        for page_config in load_configs():
            try:
                reviewed_listings = {}
                file_path = f'JSON/{page_config.key}.json'
                if not path.exists(file_path):
                    with open(file_path, "w") as file:
                        file.write("{}")
                
                with open(file_path) as json_file:
                    reviewed_listings = json.load(json_file)

                listings = Listings(reviewed_listings)
                parser = Parsers(page_config, listings)
                parser.parse()
                
                email_msg = listings.generate_email()
                if email_msg != '':
                    Mail().set_parameters_listings(page_config, email_msg).send()
                
                with open(file_path, 'w') as fp:
                    json.dump(listings.get_reviewed_listings(), fp)
                
            except Exception as e:
                mail_body = 'Error occured while running script for nepremicnine scrapper.\n' + str(e)
                Mail().set_parameters_error(
                        page_config.from_email,
                        page_config.gmail_api_key,
                        page_config.admin_mail,
                        "Nepremicnine scrapper error occured",
                        mail_body).send()

    except Exception as e:
        mail_body = 'Error occured while running batch script for nepremicnine scrapper.\n' + str(e)
        Mail().set_parameters_error(
                page_config.from_email,
                page_config.gmail_api_key,
                page_config.admin_mail,
                "Nepremicnine scrapper batch error occured",
                mail_body).send()

if __name__ == "__main__":
    main()
