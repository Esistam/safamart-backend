{
    'name': "Product Controller Apis",
    'summary': """This module will add a record to store student details""",
    'version': '16.0',
    'description': """This is a module for the extension of the products api""",
    'author': '@The-Kadweka',
    # 'company': 'Cybrosys Techno Solutions',
    # 'website': 'https://www.cybrosys.com',
    'category': 'Tools',
    'depends': ['base','account','sale_management','stock','product'],
    'license': 'AGPL-3',
    'data': [
        "views/productTemplate.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}