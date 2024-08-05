# ToSsed[https://tossed-away.vercel.app]
A user-rights initiative, powered by AI!

<br/>

## Local Download Instructions
Go to your terminal and cd into a seperate folder:
<br/>
<code>git clone https://github.com/Animatnetic/ToSsed/</code>

Then, 
<code>pip install -r requirements.txt</code>

Go to <code>.env.dist</code> and replace the <code>PUT_API_KEY_HERE</code> string with your API key, ensure it is in a string format. Then delete the <code>.dist</code> part of the filename


<br/>


## Hosting information
This project is hosted on Vercel. The front end is simply bootstrap installed via the cdn on load time so you do not need to install that.

For you to host it, here are API endpoints I pointed out for your convenience to change for your use case:

**line 92** of `summarize.js`: `https://tossed-away.vercel.app/summarize` can be changed to your URL to access your backend.
<br/>
<br/>
That's it, that's the only URL called on by the front-end that can vary.
<br/>
(Remember, you only need to do that if you are hosting this yourself.)
