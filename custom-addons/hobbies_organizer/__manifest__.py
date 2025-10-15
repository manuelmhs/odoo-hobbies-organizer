# Module basic structure created with odoo scaffold
# https://www.odoo.com/documentation/19.0/developer/reference/cli.html?highlight=scaffold#scaffold-scaffold-a-module

{
    'name': "Hobbies Organizer",

    'summary': "Organize hobbies and visualize them in a personal calendar",

    'description': """
This module allows users to manage their hobbies and schedules. 
You can assign multiple hobbies to partners, define weekly schedules with start and end times, 
and view all activities in the calendar. It also supports data validation to prevent 
overlapping activities and provides demo data for quick setup and testing.
    """,

    'author': "My Company",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '1.0',

    # any module necessary for this one to work correctly
    # in this case, odoo's base module contains all dependencies, such as the res.partner model
    'depends': ['base'],

    # always loaded
    # this includes security rules and access, .xml views and basic data loaded when the module is installed
    'data': [
        'security/ir.model.access.csv',
        'views/hobby.xml',
        'views/hobby_type.xml',
        'views/partner_hobby.xml',
        'views/partner_hobby_dayt.xml',
        'views/res_partner.xml',
        'views/menus.xml',
        'data/hobbies_data.xml'
    ],
    # only loaded in demonstration mode
    # to use these, you have to set up the odoo database to load demo data
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/partner_hobby_demo.xml',
        'demo/partner_hobby_dayt_demo.xml',
    ],
    # marks this module as an app (not only a technical module)
    'application': True,
    'installable': True
}

