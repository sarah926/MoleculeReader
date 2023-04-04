from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import io

from urllib.parse import urlparse
import urllib
import MolDisplay
import molsql
file_list = ['/listPage.html', '/style.css', '/test.js'];
header = """<html><head><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script><link rel="stylesheet" type="text/css" href="style.css" /></head>\n<body><script src="test.js"></script>""";
footer = """</body></html>""";
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
            self.wfile.write( bytes( page, "utf-8" ) );
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
            try:
                # self.send_response(200);
                # #getting data
                # content_length = int(self.headers['Content-Length']);
                # body = self.rfile.read(content_length);

                # print( repr( body.decode('utf-8') ) );

                # # convert POST content into a dictionary
                # postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

                # print( postvars );

                #if(document.getElementById(""))
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

            except:
                print("incorrect file")
                self.send_response(200);
                self.send_header("Content-type", "text/html");
                self.send_header("Content-length", len(alert));
                self.end_headers();
                self.wfile.write(bytes(alert, "utf-8"));
        elif self.path == "/home":
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(web_form));
            self.end_headers();
            self.wfile.write(bytes(web_form, "utf-8"));
        elif self.path =="/mol_list":
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
            self.send_header("Content-length", len(elemList) + len(element_list_helper) + len(header) + len(footer));
            self.end_headers();
            self.wfile.write(bytes(header, "utf-8"));
            self.wfile.write(bytes(element_list_helper, "utf-8"));
            self.wfile.write(bytes(elemList, "utf-8"));
            self.wfile.write(bytes(footer, "utf-8"));
        elif self.path == "/test":
            content_length = int(self.headers['Content-Length']);
            
            body = self.rfile.read(content_length);
            # #print(body)
            print( repr( body.decode('utf-8') ) );
            
            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( repr(body.decode( 'utf-8' ) ));
        
            #requests.post('https://httpbin.org/post', data={'key':'value'})
            print( postvars );
            #VALIDATE DATA FIRST

            #take of leading and ending parentheses
            elCode = postvars['elCode'][0];
            elCode = elCode[:-1]
            values = (postvars['elNum'][0], elCode, postvars["'elName"][0], postvars['color1'][0], postvars['color2'][0], postvars['color3'][0], postvars['radius'][0])
            print(values)
            works = self.db.validateElement(values);
            if(works == True):
                try:
                    self.db.__setitem__("Elements", values);
                except:
                    print("unique failed");
            else:
                print("Incorect")
            self.send_response(200);
            elemList = self.db.makeElementListSVG();
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(elemList) + len(element_list_helper) + len(header) + len(footer));
            self.end_headers();
            self.wfile.write(bytes(header, "utf-8"));
            self.wfile.write(bytes(element_list_helper, "utf-8"));
            self.wfile.write(bytes(elemList, "utf-8"));
            self.wfile.write(bytes(footer, "utf-8"));
            
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));

web_form = """
<html style="background-color:#b4caf0">
    <head>
        <title> File Upload </title>
        <link rel="stylesheet" type="text/css" href="style.css" />
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
            <h2>Molecule Name:</h2>
            <h3>[must be unique]</h3>
            <p>
                <input id="molName" />
            </p>
        </form>
        <form action="mol_list" enctype="multipart/form-data" method="post">
            <button type="submit" value="View List" id="viewListButton"> View Molecule List</button> 
        </form>
        <form action="element_list" enctype="multipart/form-data" method="post">
            <button type="submit" id="viewListButton">View Element List</button> 
        </form>
    </body>
</html>
"""
alert = """<html>
    <div class="alert">incorrectly formatted file</div>
    <form action="home" enctype="multipart/form-data" method="post">
        <button type="submit" value="home" id="homeButton"> Try Again</button> 
    </form>
</html>"""
element_list_helper = """
    <h1>Add Element to List</h1>
    <form action="test"  method="post">
        <p>
            <label>Element Name:<input id="elName" name="elName"/></label>
            <label>Element Number:<input id="elNum" name="elNum"/></label>
        </p>
        <p>
            <label>Colour 1:<input id="color1" name="color1"/></label>
            <label>Colour 2:<input id="color2" name="color2"/></label>
            <label>Colour 3:<input id="color3" name="color3"/></label>
        </p>
        <p>
            <label>Radius:<input id="radius" name="radius"/></label>
            <label>Element Code:<input id="elCode" name = "elCode"/></label>
        </p>
        <button type ="submit" id="addElementButton">Add Element</button>
    </form>
    <h2>Remove Element:</h2>
    <form action="test" enctype="multipart/form-data" method="post">
        <p>
            <label>Number in List to Remove:<input id="removeCode"/></label>
        </p>
        <button type ="submit" id="removeElementButton" onclick="formFilled()">Remove Element</button>
    </form>
    <form action="home" enctype="multipart/form-data" method="post">
        <button type="submit" id="back">Back</button>
    </form>
    <h2>Current Element List</h2>
"""
httpd = HTTPServer(('localhost', int(sys.argv[1])), Server);
print("opened server" + sys.argv[1] + "\n");
httpd.serve_forever();