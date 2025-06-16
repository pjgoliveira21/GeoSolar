import os
from factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=os.environ.get('MYADDR'), port=int(os.environ.get('MYPORT')), debug=True)
    
