from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import io
import MolDisplay
import molsql
file_list = ['/listPage.html', '/style.css'];
class Server(BaseHTTPRequestHandler):
    db = molsql.Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    rad = db.radius();
    el = db.element_name();
    grad = db.radial_gradients();
    def do_GET(self):
        if self.path in file_list:
            print("in style")
            self.send_response( 200 );  # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( self.path[1:] ); 
            # [1:] to remove leading / so that file is found in current dir

            # load the specified file
            page = fp.read();
            fp.close();

            # create and send headers
            self.send_header( "Content-length", len(page) );
            self.end_headers();
        elif self.path == "/":
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(web_form));
            self.end_headers();
            self.wfile.write(bytes(web_form, "utf-8"));
            #self.wfile.close()
        elif self.path.startswith("/view/"):
            self.send_response(200);
            molName = self.path[6:];
            tempMol = self.db.load_mol(molName);
            self.send_header("Content-type", "image/svg+xml");
            self.end_headers();
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            self.wfile.write(bytes(tempMol.svg(rad, el, grad), "utf-8"));
        
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));
    def do_POST(self):
        if self.path == "/molecule":
            self.send_response(200);
            #if(document.getElementById(""))
            file = self.rfile.read(int(self.headers['Content-length']));
            tempMol = MolDisplay.Molecule();
            stringcontents = file.decode("utf-8");
            stringiostream = io.StringIO(stringcontents);
            stringiostream.readline();
            stringiostream.readline();
            stringiostream.readline();
            stringiostream.readline();
            tempMol.parse(stringiostream);
            stringiostream.seek(0,0)
            stringiostream.readline();
            stringiostream.readline();
            stringiostream.readline();
            stringiostream.readline();
            self.db.add_molecule(self.headers['Content-length'], stringiostream);
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            self.send_header("Content-type", "image/svg+xml");
            self.end_headers();
            #self.wfile.write(bytes(self.grad, "utf-8"));
            self.wfile.write(bytes(tempMol.svg(rad, el, grad), "utf-8"));
        elif self.path =="/list":
            print("list")
            list = self.db.makeMolListSVG();
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(list));
            self.end_headers();
            self.wfile.write(bytes(list, "utf-8"));
        elif self.path == "/element_list":
            self.send_response(200);
            elemList = self.db.makeElementListSVG();
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(elemList));
            self.end_headers();
            self.wfile.write(bytes(elemList, "utf-8"));
       
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));

web_form = """
<html>
    <head>
        <title> File Upload </title>
        <link rel="stylesheet" type="text/css" href="styles.css" />
    </head>
    <body>
        <h1> File Upload </h1>
        <form action="molecule" enctype="multipart/form-data" method="post">
            <p>
                <input type="file" id="sdf_file" name="filename"/>
            </p>
            <p>
                <input type="submit" value="Upload"/>
            </p> 
            <h2>Molecule Name: [must be unique]</h2>
            <p>
                <input id="molName"/>
            </p>
        </form>
        <form action="list" enctype="multipart/form-data" method="post">
            <button type="submit" value="View List" id="viewListButton"> View Molecule List</button> 
        </form>
        <form action="element_list" enctype="multipart/form-data" method="post">
            <button type="submit" id="viewListButton">View Element List</button> 
        </form>
    </body>
</html>
"""

httpd = HTTPServer(('localhost', int(sys.argv[1])), Server);
print("opened server" + sys.argv[1] + "\n");
httpd.serve_forever();