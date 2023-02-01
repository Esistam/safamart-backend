{
    'name': "Money Management",
    'summary': """This module will add a record to store student details""",
    'version': '15.0',
    'description': """This module will add a record to store student details""",
    'author': '@The-Kadweka',
    # 'company': 'Cybrosys Techno Solutions',
    # 'website': 'https://www.cybrosys.com',
    'category': 'Tools',
    'depends': ['base','contacts','ooh_customer_auth'],
    'license': 'AGPL-3',
    'data': [
        'views/views.xml',
        'views/configuration.xml',
        'views/sequence.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}