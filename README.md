# python-webserver

This repository demonstrates how to connect any Python web framework (Flask, Pyramid) or application with a single server without needing to change its code.

This type of interface is known as a WSGIServer, and it is written in `webserver.py`.

To run this demo:
`git clone git@github.com:zyam/python-webserver.git`

`cd python-webserver`

Make sure both Flask and Pyramid are installed locally. To do that:
`[sudo] pip install virtualenv`

`mkdir ~/envs`

`virtualenv ~/envs/lsbaws/`

`cd ~/envs/lsbaws/`

`source bin/activate`

`(lsbaws) $ pip install pyramid`

`(lsbaws) $ pip install flask`

Once installed, cd back into the repository

Run the webserver with the pyramid app
`(lsbaws) $ python webserver.py pyramidapp:app`

Open your browser and head to `http://localhost:8888/hello`

You should see the response: `Hello world from Pyramid!`

Next, run the webserver with the flask app
`(lsbaws) $ python webserver.py flasapp:app`

You should now see the response change to: `Hello world from Flask!`
