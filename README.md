# gluer
Builds a "module" for a website using [Gluon](https://github.com/gluon-framework/gluon) and builds shortcuts for GNOME.

## Requirements
 - Globally-installed gluon (`npm install -g @gluon-framework/gluon`) 
   - Well, ideally. For now, you need to install per-app.
 - Python 3.9 (unknown, likely safe to use 3.7 - 3.X)
## Usage
`python3 gluer.py url-to-make name-of-app`  
For example, to make a bundled version of Apple Music Web:
`python3 gluer.py https://music.apple.com 'Apple Music'`

Run the generated `install.sh` and enjoy your "native" app!