import json
from os import path

from helpers.listings import Listings
from helpers.mail import Mail
from helpers.parsers.parsers import Parsers

from helpers.page import load_json, PageConfiguration, MailConfig

def main():
    try:
        config = load_json()
        print(config)
        for page_config in config.requests:
            # run_single('', page_config, config.mail)
            pass
        
        for page_config in config.json:
            pass

        for page_config in config.selenium:
            pass 

    except Exception as e:
        mail_body = 'Error occured while running batch script for nepremicnine scrapper.\n' + str(e)
        Mail().set_parameters_error(
                config.mail.from_email,
                config.mail.gmail_api_key,
                config.mail.admin_mail,
                'Nepremicnine scrapper batch error occured',
                mail_body).send()


    def run_single(parser_type: str, page_config, mail_config: MailConfig):
        try:
            reviewed_listings = {}
            file_path = f'JSON/{page_config.key}.json'
            if not path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.write('{}')
            
            with open(file_path) as json_file:
                reviewed_listings = json.load(json_file)

            listings = Listings(reviewed_listings)
            parser = Parsers(parser_type, page_config, listings)
            parser.parse()
            
            email_msg = listings.generate_email()
            if email_msg != '':
                Mail().set_parameters_listings(mail_config, page_config, email_msg).send()
            
            with open(file_path, 'w') as fp:
                json.dump(listings.get_reviewed_listings(), fp)
            
        except Exception as e:
            mail_body = 'Error occured while running script for nepremicnine scrapper.\n' + str(e)
            Mail().set_parameters_error(
                    mail_config.from_email,
                    mail_config.gmail_api_key,
                    mail_config.admin_mail,
                    'Nepremicnine scrapper error occured',
                    mail_body).send()


if __name__ == '__main__':
    main()
