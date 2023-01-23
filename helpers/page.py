import json
from typing import List, Any, TypeVar, Callable, Type, cast

import helpers.config_defaults as defaults


T = TypeVar("T")


def from_str(x: Any) -> str:
    if x is None:
        return None
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if x is None:
        return None
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    if x is None:
        return None
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class BaseConfig:
    key: str
    default_url: str
    page_url: str
    to_email: List[str]
    mail_subject: str

    def __init__(self, base_config: 'BaseConfig') -> None:
        if base_config:
            self.key = base_config.key
            self.default_url = base_config.default_url
            self.page_url = base_config.page_url
            self.to_email = base_config.to_email
            self.mail_subject = base_config.mail_subject
    
    @staticmethod
    def from_dict(obj: Any) -> 'BaseConfig':
        assert isinstance(obj, dict)

        base_config = BaseConfig(None)
        base_config.key = from_str(obj.get("key"))
        base_config.default_url = from_str(obj.get("default_url"))
        base_config.page_url = from_str(obj.get("page_url"))
        base_config.to_email = from_list(from_str, obj.get("to_email"))
        base_config.mail_subject = from_str(obj.get("mail_subject"))
        
        return base_config
    
    def to_dict(self) -> dict:
        result: dict = {}

        result["key"] = from_str(self.key)
        result["default_url"] = from_str(self.default_url)
        result["page_url"] = from_str(self.page_url)
        result["to_email"] = from_list(from_str, self.to_email)
        result["mail_subject"] = from_str(self.mail_subject)

        return result


class MailConfig:
    from_email: str
    gmail_api_key: str
    admin_mail: List[str]

    def __init__(self, from_email: str, gmail_api_key: str, admin_mail: List[str]) -> None:
        self.from_email = from_email
        self.gmail_api_key = gmail_api_key
        self.admin_mail = admin_mail

    @staticmethod
    def from_dict(obj: Any) -> 'MailConfig':
        assert isinstance(obj, dict)

        from_email = from_str(obj.get("from_email"))
        gmail_api_key = from_str(obj.get("gmail_api_key"))
        admin_mail = from_list(from_str, obj.get("admin_mail"))
        
        return MailConfig(from_email, gmail_api_key, admin_mail)

    def to_dict(self) -> dict:
        result: dict = {}

        result["from_email"] = from_str(self.from_email)
        result["gmail_api_key"] = from_str(self.gmail_api_key)
        result["admin_mail"] = from_list(from_str, self.admin_mail)
        
        return result


class PageJson(BaseConfig):
    request_method: str
    post_body: str
    url_attributes: str
    info_attributes: str
    pagination_name: str
    pagination_offset: int
    pagination_offset_name: str
    pagination_limit: int
    pagination_limit_name: str
    pagination_count_all_name: str
    result_name: str

    def __init__(self, base_config: BaseConfig, request_method: str, post_body: str,
                url_attributes: str, info_attributes: str, pagination_name: str,
                pagination_offset: int, pagination_offset_name: str, pagination_limit: int,
                pagination_limit_name: str, pagination_count_all_name: str, result_name: str) -> None:
        super().__init__(base_config)

        self.request_method = request_method
        self.post_body = post_body
        self.url_attributes = url_attributes
        self.info_attributes = info_attributes
        self.pagination_name = pagination_name
        self.pagination_offset = pagination_offset
        self.pagination_offset_name = pagination_offset_name
        self.pagination_limit = pagination_limit
        self.pagination_limit_name = pagination_limit_name
        self.pagination_count_all_name = pagination_count_all_name
        self.result_name = result_name

    @staticmethod
    def from_dict(obj: Any) -> 'PageJson':
        assert isinstance(obj, dict)

        base_config = BaseConfig.from_dict(obj)

        request_method = from_str(obj.get("request_method"))
        post_body = from_str(obj.get("post_body"))
        url_attributes = from_str(obj.get("url_attributes"))
        info_attributes = from_str(obj.get("info_attributes"))
        pagination_name = from_str(obj.get("pagination_name"))
        pagination_offset = int(from_str(obj.get("pagination_offset")))
        pagination_offset_name = from_str(obj.get("pagination_offset_name"))
        pagination_limit = int(from_str(obj.get("pagination_limit")))
        pagination_limit_name = from_str(obj.get("pagination_limit_name"))
        pagination_count_all_name = from_str(obj.get("pagination_count_all_name"))
        result_name = from_str(obj.get("result_name"))
        
        return PageJson(base_config, request_method, post_body, url_attributes, info_attributes,
                        pagination_name, pagination_offset, pagination_offset_name, pagination_limit,
                        pagination_limit_name, pagination_count_all_name, result_name)

    def to_dict(self) -> dict:
        result: dict = BaseConfig.to_dict(self)

        result["key"] = from_str(self.key)
        result["default_url"] = from_str(self.default_url)
        result["page_url"] = from_str(self.page_url)
        result["mail_subject"] = from_str(self.mail_subject)
        result["to_email"] = from_list(from_str, self.to_email)
        result["request_method"] = from_str(self.request_method)
        result["post_body"] = from_str(self.post_body)
        result["url_attributes"] = from_str(self.url_attributes)
        result["info_attributes"] = from_str(self.info_attributes)
        result["pagination_name"] = from_str(self.pagination_name)
        result["pagination_offset"] = from_str(str(self.pagination_offset))
        result["pagination_offset_name"] = from_str(self.pagination_offset_name)
        result["pagination_limit"] = from_str(str(self.pagination_limit))
        result["pagination_limit_name"] = from_str(self.pagination_limit_name)
        result["pagination_count_all_name"] = from_str(self.pagination_count_all_name)
        result["result_name"] = from_str(self.result_name)

        return result


class Bs4Attrs:
    bs4_attrs_class: str
    itemtype: str

    def __init__(self, bs4_attrs_class: str, itemtype: str) -> None:
        self.bs4_attrs_class = bs4_attrs_class
        self.itemtype = itemtype

    @staticmethod
    def from_dict(obj: Any) -> 'Bs4Attrs':
        if obj is None:
            return None
        
        assert isinstance(obj, dict)

        bs4_attrs_class = from_str(obj.get("class"))
        itemtype = from_str(obj.get("itemtype"))
        
        return Bs4Attrs(bs4_attrs_class, itemtype)

    def to_dict(self) -> dict:
        result: dict = {}
        
        result["class"] = from_str(self.bs4_attrs_class)
        result["itemtype"] = from_str(self.itemtype)
        
        return result


class Attributes:
    bs4_block: str
    bs4_attrs: Bs4Attrs
    bs4_class: str

    def __init__(self, bs4_block: str, bs4_attrs: Bs4Attrs, bs4_class: str) -> None:
        self.bs4_block = bs4_block
        self.bs4_attrs = bs4_attrs
        self.bs4_class = bs4_class

    @staticmethod
    def from_dict(obj: Any) -> 'Attributes':
        assert isinstance(obj, dict)
        
        bs4_block = from_str(obj.get("bs4_block"))
        bs4_attrs = Bs4Attrs.from_dict(obj.get("bs4_attrs"))
        bs4_class = from_str(obj.get("bs4_class"))
        
        return Attributes(bs4_block, bs4_attrs, bs4_class)

    def to_dict(self) -> dict:
        result: dict = {}

        result["bs4_block"] = from_str(self.bs4_block)
        result["bs4_attrs"] = to_class(Bs4Attrs, self.bs4_attrs)
        result["bs4_class"] = from_str(self.bs4_class)
        
        return result


class PageRequest(BaseConfig):
    bs4_block: str
    href_parser: str
    bs4_attrs: Bs4Attrs
    info_attributes: Attributes
    summary_attributes: Attributes

    def __init__(self, base_config: BaseConfig, bs4_block: str,
                href_parser: str, bs4_attrs: Bs4Attrs, info_attributes: Attributes,
                summary_attributes: Attributes) -> None:
        super().__init__(base_config)
        
        self.bs4_block = bs4_block
        self.href_parser = href_parser
        self.bs4_attrs = bs4_attrs
        self.info_attributes = info_attributes
        self.summary_attributes = summary_attributes

    @staticmethod
    def from_dict(obj: Any) -> 'PageRequest':
        assert isinstance(obj, dict)

        base_config = BaseConfig.from_dict(obj)

        bs4_block = from_str(obj.get("bs4_block"))
        href_parser = from_str(obj.get("href_parser"))
        bs4_attrs = Bs4Attrs.from_dict(obj.get("bs4_attrs"))
        info_attributes = Attributes.from_dict(obj.get("info_attributes"))
        summary_attributes = Attributes.from_dict(obj.get("summary_attributes"))
        
        return PageRequest(base_config, bs4_block, href_parser, bs4_attrs, info_attributes, summary_attributes)

    def to_dict(self) -> dict:
        result: dict = BaseConfig.to_dict(self)

        result["bs4_block"] = from_str(self.bs4_block)
        result["href_parser"] = from_str(self.href_parser)
        result["bs4_attrs"] = to_class(Bs4Attrs, self.bs4_attrs)
        result["info_attributes"] = to_class(Attributes, self.info_attributes)
        result["summary_attributes"] = to_class(Attributes, self.summary_attributes)

        return result


class PageConfiguration:
    requests: List[PageRequest]
    json: List[PageJson]
    selenium: List[Any]
    mail: MailConfig

    def __init__(self, requests: List[PageRequest], json: List[PageJson], selenium: List[Any], mail: MailConfig) -> None:
        self.requests = requests
        self.json = json
        # self.selenium = selenium
        self.mail = mail

        for r in requests:
            r.mail = self.mail
        
        for j in json:
            j.mail = self.mail

    @staticmethod
    def from_dict(obj: Any) -> 'PageConfiguration':
        assert isinstance(obj, dict)
        
        requests = from_list(PageRequest.from_dict, obj.get("requests"))
        json = from_list(PageJson.from_dict, obj.get("json"))
        selenium = from_list(lambda x: x, obj.get("selenium"))
        mail = MailConfig.from_dict(obj.get("mail"))

        return PageConfiguration(requests, json, selenium, mail)

    def to_dict(self) -> dict:
        result: dict = {}
        
        result["requests"] = from_list(lambda x: to_class(PageRequest, x), self.requests)
        result["json"] = from_list(lambda x: to_class(PageJson, x), self.json)
        result["selenium"] = from_list(lambda x: x, self.selenium)
        result["mail"] = to_class(MailConfig, self.mail)
        return result


def load_json() -> PageConfiguration:
    with open('./configuration.json') as json_file:
        return PageConfiguration.from_dict(json.loads(json_file.read()))


def dump_json(x: PageConfiguration) -> Any:
    return to_class(PageConfiguration, x)



# def check_fields(page: Dict) -> None:
#     keys = ['key', 'to_email', 'from_email', 'default_url', 'page_url', 'gmail_api_key']
#     for key in keys:
#         if key not in page:
#             raise Exception(f'Missing {key} parameter in configuration')