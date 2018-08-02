==============================================
Errbot as an interface to StackStorm's ChatOps
==============================================

.. contents::
    :local:

Deploy `Errbot`_ using `docker-compose`_ connected with `StackStorm`_ to fully
leverage its `ChatOps`_ capabilities in `Slack`_.

.. _`Errbot`: https://github.com/errbotio/errbot
.. _`docker-compose`: https://github.com/docker/compose
.. _`StackStorm`: https://github.com/StackStorm/st2
.. _`ChatOps`: https://docs.stackstorm.com/chatops/index.html
.. _`Slack`: https://slack.com/

TL;DR
=====

#. Deploy and configure StackStorm:

   .. code:: bash

       git clone https://github.com/StackStorm/st2-docker.git
       cd st2-docker
       make env
       docker-compose up -d
       docker-compose exec stackstorm bash
       # Save the key to put in ST2_API_KEY later
       st2 apikey create -k -m '{"used_by": "my Errbot"}'
       cd /opt/stackstorm/packs/chatops/rules/
       sed -i -e '/^enabled: / s/true/false/' notify_hubot.yaml
       wget https://raw.githubusercontent.com/fmnisme/err-stackstorm/master/contrib/stackstorm-chatops/rules/notify_errbot.yaml
       cd ../actions
       sed -i -e '/^\s\+default: / s/chatops/errbot/' post_message.yaml
       st2ctl reload
       exit

#. Deploy Errbot container:

   .. code:: bash

       git clone --recurse-submodules https://github.com/vutny/errbot-slack-st2.git
       cd errbot-slack-st2
       export SLACK_API_TOKEN='xoxb-123456789098-QwErTyUiOpaSdFgHjKlZxCvB'
       export ERRBOT_ADMINS='@denys'  # Put your username in a chat here
       export ST2_API_KEY='MGU5NjQ2YzM2NzgwNDQxNmQ2MjI1ZjJkNzZlMGNlYm...'
       [ "$(uname -s)" = "Darwin" ] && export ST2_HOST=192.168.65.1
       docker-compose up -d

#. Check the Errbot is alive by sending it direct message in Slack:

   .. code:: console

       !st2help

Requirements
============

Docker
------

Minimum required versions are:

* Docker 1.13.1 (or later Docker CE)
* docker-compose 1.17.1

Slack
-----

Create a bot integration in your Slack Team.

#. Go to team menu, select **Customize Slack** option.
#. In **Customize Your Workspace** page menu, click on **Configure Apps**.
#. Select **Custom Integrations** and then **Bots**.
#. Create new integration. Depending on a Slack team settings, you may need to
   issue a **Request to Install** a bot from Slack Workspace Owner.
#. Copy the **API token**, we will need it to configure our Errbot.
#. Give your new bot a fun name and describe what it does.
#. Press **Save Integration**.

StackStorm
----------

You need to install StackStorm and configure `API Key`_ for Errbot to be able
to talk to it.  Use ``st2 apikey create`` command inside the ``stackstorm``
container to generate it.

The best option for local testing and development is `getting Docker`_, but you
may consider to have a full-fledged installation from the upstream packages on
a dedicated or virtual machine.

.. _`API Key`: https://docs.stackstorm.com/authentication.html#api-keys
.. _`getting Docker`: https://github.com/StackStorm/st2-docker

Deployment
==========

ChatOps Support Pack
--------------------

Some additional configuration for ``chatops`` pack in StackStorm required for
Errbot to be able to receive event streams back with command execution results.
Create new ``notify-errbot`` rule and change the route in ``post_message``
action as listed above.

Configuration
-------------

Before spinning up Errbot, few environment variables must be configured.

* ``BOT_ADMINS``: account names of user who would be allowed to issue
  administrative commands to Errbot.
* ``BOT_TOKEN``: API token for existing or newly created custom bot
  integration in Slack, see above.
* ``CORE_PLUGINS`` (optional): specify which bundled plugins Errbot should load
  on start up, separated by comma.
  ``ST2_API_KEY``: the key created in StackStorm to access its API.
* ``ST2_HOST`` (optional): if you're running StackStorm in **Docker on MacOS**
  set it to ``192.168.65.1``. This is special loopback interface IP address.

You could export these variables in shell session or save them to ``.env`` file
in the root of the repository.

Plugins
-------

During the first start of the ``errbot`` service container,
`WebserverConfiguration`_ and `err-stackstorm`_ plugins will be automagically
activated exposing StackStorm's `Action Aliases`_ to Errbot.

.. _`WebserverConfiguration`: https://github.com/tkit/errbot-plugin-webserverconfiguration
.. _`err-stackstorm`: https://github.com/fmnisme/err-stackstorm
.. _`Action Aliases`: https://docs.stackstorm.com/chatops/aliases.html

Launch
------

Start the container with pre-configured Slack and StackStorm integration:

.. code:: bash

    docker-compose up -d

.. vim: fenc=utf-8 spell spl=en cc=80 tw=79 fo=want sts=4 sw=4 et
