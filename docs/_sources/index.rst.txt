********
Source Code Description
********


Heroku automatically runs jobs defined in Procfile after deployment. The FAQ bot's Procfile initializes the environment and runs main.py to run daemons.

In this section, we'll describe functions using APIs in the FAQ bot.

Example) The source code of faq_bot.externals.contacts.get_account_info is in the get_account_info function in faq_bot/externals/contacts.py.

Development Language and Environment
=================

The following shows the required development environment and language:

- Python3
- Tornado framework

Procfile
========

https://devcenter.heroku.com/articles/procfile:

    Heroku apps include a Procfile that specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including:
    - Your app’s web server
    - Multiple types of worker processes
    - A singleton process, such as a clock
    - Tasks to run before a new release is deployed

This bot's Procfile:

.. literalinclude:: ../Procfile
    :caption: Procfile

Run bot
=======

.. literalinclude:: ../main.py
    :caption: main.py

.. autofunction:: faq_bot.faq_bot.start_faq_bot
    :noindex:

.. autofunction:: faq_bot.router.getRouter
    :noindex:

.. autoclass:: faq_bot.callbackHandler.CallbackHandler
    :members:
    :noindex:

.. autoclass:: faq_bot.check_and_handle_actions.CheckAndHandleActions
    :members:
    :noindex:

Register bot
------------

.. autofunction:: faq_bot.register_bot.init_bot
    :noindex:

.. autofunction:: faq_bot.register_bot.get_message_bot_from_remote
    :noindex:

.. autofunction:: faq_bot.register_bot.register_bot
    :noindex:

.. autofunction:: faq_bot.register_bot.register_bot_domain
    :noindex:


Bot API functions
=================

.. autofunction:: faq_bot.model.data.make_text
    :noindex:

.. autofunction:: faq_bot.model.data.make_quick_reply
    :noindex:

.. autofunction:: faq_bot.model.data.make_carousel
    :noindex:

.. autofunction:: faq_bot.model.data.make_list_template
    :noindex:

.. autofunction:: faq_bot.externals.send_message.push_message
    :noindex:

Home API functions
======================

.. autofunction:: faq_bot.externals.home.create_boards
    :noindex:

.. autofunction:: faq_bot.externals.home.get_boards
    :noindex:

.. autofunction:: faq_bot.externals.home.create_articles
    :noindex:

.. autofunction:: faq_bot.externals.home.init_board
    :noindex:

Bot rich menu functions
=======================

.. autofunction:: faq_bot.externals.richmenu.init_rich_menu
    :noindex:

.. autofunction:: faq_bot.externals.richmenu.upload_content
    :noindex:

.. autofunction:: faq_bot.externals.richmenu.make_add_rich_menu_body
    :noindex:

.. autofunction:: faq_bot.externals.richmenu.set_rich_menu_image
    :noindex:

.. autofunction:: faq_bot.externals.richmenu.set_user_specific_rich_menu
    :noindex:

.. autofunction:: faq_bot.externals.richmenu.get_rich_menus
    :noindex:

.. autofunction:: faq_bot.externals.richmenu.cancel_user_specific_rich_menu
    :noindex:

Bot i18n functions
===================

You can use the. /tools/gen.sh tool to generate '. Po', '. Mo' files.

    reference
    - https://docs.python.org/2/library/gettext.html
    - test/test_i18.py

execute
-------

    $ ./tools/gen.sh [filename] [po|mo] [path]

========    ===========
paramter    description
========    ===========
filename    Python source filename used to generate '.po','.mo'.
type        'po' means generate '.po' file, 'mo' means generate '.mo' file
path        Relative directory of Python source files. not ending with '/'.
========    ===========

You can find the corresponding '.po' file in 'locales/../LC_MESSAGES' according to your source file name.

step
----
1. generate '.po' file.
    ./tools/gen.sh test_i18n.py po test<br/>
    check: locales/../LC_MESSAGES/test_i18n.po
2. Multilingual string to fill in '.po' file.
3. generate '.mo' file
    ./tools/gen.sh test_i18n.py mo test<br/>
    check: locales/../LC_MESSAGES/test_i18n.mo

.. autofunction:: faq_bot.model.i18n_data.get_i18n_content_by_lang
    :noindex:

.. autofunction:: faq_bot.model.i18n_data.get_i18n_content
    :noindex:

.. autofunction:: faq_bot.model.i18n_data.make_i18n_button
    :noindex:

.. autofunction:: faq_bot.model.i18n_data.make_i18n_text
    :noindex:

.. autofunction:: faq_bot.model.i18n_data.make_i18n_message_action
    :noindex:

.. autofunction:: faq_bot.model.i18n_data.make_i18n_carousel_column
    :noindex:

.. autofunction:: faq_bot.model.i18n_data.make_i18n_list_template_element
    :noindex:

Set Language Code for Event Subject
===================================

The faq bot basically creates a Find "FAQ" by task/Send a question event subject in Japanese. If necessary, you can change the language code for event subjects to Korean or English.

To do so, edit # default language in config.py under the conf folder as shown below.

DEFAULT_LANG =”{Language code}”

    Note
    - You can choose among kr (Korean), ja (Japanese), and en (English).

Indices and tables
==================

.. toctree::
    :maxdepth: 4

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
