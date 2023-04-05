from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import io
import random

from urllib.parse import urlparse
import urllib
import MolDisplay
import molsql
file_list = ['/listPage.html', '/style.css', '/test.js'];
header = """<html><head><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script><link rel="stylesheet" type="text/css" href="style.css" /></head>\n<body><script src="test.js"></script>""";
footer = """</body></html>""";
global name;
name = "yo";
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
        #LOADS NECESSARY FILES
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
        #BEGINNING PATH
        elif self.path == "/":
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(web_form));
            self.end_headers();
            self.wfile.write(bytes(web_form, "utf-8"));
            #self.wfile.close()
        #FOR VIEWING SPECIFIC MOLECULE BASED ON NAME
        elif self.path.startswith("/view/"):
            self.send_response(200);
            molName = self.path[6:];
            tempMol = self.db.load_mol(molName);
            self.send_header("Content-type", "image/svg+xml");
            self.end_headers();
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            tempMol.sort();
            #self.wfile.write(bytes(tempMol, "utf-8"));
            self.wfile.write(bytes(tempMol.svg(rad, el, grad), "utf-8"));
        elif self.path.startswith("/viewer"):
            molName = self.path[7:];
            print(molName);
            mol = self.db.load_mol(molName);
            self.send_header("Content-type", "image/svg+xml");
            self.end_headers();
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            #self.wfile.write(bytes(self.grad, "utf-8"));
            self.wfile.write(bytes(mol.svg(rad, el, grad), "utf-8"));
        #IF INVALID
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));
    def do_POST(self):
        #IF CHOSE A MOLECULE FILE TO LOAD
        if self.path.startswith("/molecule"):
            try:
                if self.path.startswith("/molecule"):
                    molName = self.path[10:];
                    if(len(molName)==0):
                        molName = "Molecule" + random.randint(0,100);
                    self.send_response(200);
                    file = self.rfile.read(int(self.headers['Content-length']));
                    print(file)
                    tempMol = MolDisplay.Molecule();
                    stringcontents = file.decode("utf-8");
                    stringiostream = io.StringIO(stringcontents);
                    stringiostream.readline();
                    stringiostream.readline();
                    stringiostream.readline();
                    stringiostream.readline();
                    tempMol.parse(stringiostream);
                    tempMol.sort();
                    stringiostream.seek(0,0)
                    stringiostream.readline();
                    stringiostream.readline();
                    stringiostream.readline();
                    stringiostream.readline();
                    self.db.add_molecule(molName, stringiostream);
                    rad = self.db.radius();
                    el = self.db.element_name();
                    grad = self.db.radial_gradients();
                    self.send_header("Content-type", "image/svg+xml");
                    self.end_headers();
                    #self.wfile.write(bytes(self.grad, "utf-8"));
                    self.wfile.write(bytes(tempMol.svg(rad, el, grad), "utf-8"));

            #CATCHES EXCEPTION IF FILE INVALID
            except:
                print("incorrect file")
                self.send_response(200);
                self.send_header("Content-type", "text/html");
                self.send_header("Content-length", len(alert));
                self.end_headers();
                self.wfile.write(bytes(alert, "utf-8"));
        #FOR RETURNING TO HOME SCREEN
        elif self.path == "/home":
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(web_form));
            self.end_headers();
            self.wfile.write(bytes(web_form, "utf-8"));
        
        #FOR UPLOADING FILES
        elif self.path.startswith("/file_upload"):
            #get post content
            content_length = int(self.headers['Content-Length']);
           
            body = self.rfile.read(content_length); 
            
            # #print(body)
            print( repr( body.decode('utf-8') ) );
            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( repr(body.decode( 'utf-8' ) ));
            print( postvars );
            print(postvars["'molName"][0][:-1]);
            name = postvars["'molName"][0][:-1];
            tempFile = file_upload
            tempFile = tempFile.replace("***", name)
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(tempFile));
            self.end_headers();
            self.wfile.write(bytes(tempFile, "utf-8"));
        
        #FOR VIEWING MOLECULE LIST
        elif self.path =="/mol_list":
            print("list")
            list = self.db.makeMolListSVG();
            self.send_response(200);
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(list));
            self.end_headers();
            self.wfile.write(bytes(list, "utf-8"));
        #FOR VIEWING ELEMENT_LIST
        elif self.path == "/element_list":
            self.send_response(200);
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            elemList = self.db.makeElementListSVG();
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(elemList) + len(element_list_helper) + len(header) + len(footer));
            self.end_headers();
            self.wfile.write(bytes(header, "utf-8"));
            self.wfile.write(bytes(element_list_helper, "utf-8"));
            self.wfile.write(bytes(elemList, "utf-8"));
            self.wfile.write(bytes(footer, "utf-8"));
        #FOR ADDING ELEMENTS
        elif self.path == "/test":
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            # #print(body)
            print( repr( body.decode('utf-8') ) );
            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( repr(body.decode( 'utf-8' ) ));
            print( postvars );

            #take of leading and ending parentheses
            elCode = postvars['elCode'][0];
            elCode = elCode[:-1]
            values = (postvars['elNum'][0], elCode, postvars["'elName"][0], postvars['color1'][0], postvars['color2'][0], postvars['color3'][0], postvars['radius'][0])
            print(values)
            #validate data
            works = self.db.validateElement(values);
            if(works == True):
                try:
                    self.db.__setitem__('Elements', values);
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
        
        #FOR REMOVING ELEMENTS
        elif self.path == "/test2":
            
            #get post content
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);
            # #print(body)
            print( repr( body.decode('utf-8') ) );
            # convert POST content into a dictionary
            postvars = urllib.parse.parse_qs( repr(body.decode( 'utf-8' ) ));
            print( postvars );
            works = self.db.validateRemoveElement(postvars["'removeCode"][0]);
            if(works == True):
                try:
                    self.db.removeElement(postvars["'removeCode"][0]);
                except:
                    print("failed");
            else:
                print("invalid")
            #update dictionaries
            rad = self.db.radius();
            el = self.db.element_name();
            grad = self.db.radial_gradients();
            #loads element list again
            self.send_response(200);
            elemList = self.db.makeElementListSVG();
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length", len(elemList) + len(element_list_helper) + len(header) + len(footer));
            self.end_headers();
            self.wfile.write(bytes(header, "utf-8"));
            self.wfile.write(bytes(element_list_helper, "utf-8"));
            self.wfile.write(bytes(elemList, "utf-8"));
            self.wfile.write(bytes(footer, "utf-8"));
        
        #PAGE NOT VALID
        else:
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: not found", "utf-8"));
rot = """ <html>
<img id="svg-object" src="/view/caff"></img>
<button type="submit" id="rotate">ROTATE</button>
"""

file_upload = """
<html style="background-color:#b4caf0">
    <form action="home" enctype="multipart/form-data" method="post">
        <button type="submit" id="back" style="font-size: 30px">BACK HOME</button>
    </form>
    <head>
        <title> File Upload </title>
        <link rel="stylesheet" type="text/css" href="style.css" />
    </head>
    <body>
        <h1> File Upload </h1>
        <form action="molecule/***" enctype="multipart/form-data" method="post">
            <p>
                <input type="file" id="sdf_file" name="filename"/>
            </p>
            <button type="submit" id="submit">Upload</button>
        </form>
    </body>
</html>
"""
web_form = """
<html style="background-color:#b4caf0">
    <head>
        <h1>Home Page</h1>
        <form action="file_upload" method="post">
        <h2>Add a molecule by entering a name:</h2>
            <p>
                <label>Enter Molecule Name: <input id="molName" name="molName"/></label>
            </p>
            <button type="submit" id="submitName"  style="font-size: 20px">Add Molecule</button>
        </form>
        <br/>
        <br/>
        <br/>
        <form action="mol_list" enctype="multipart/form-data" method="post">
            <button type="submit" value="View List" id="viewListButton"  style="font-size: 20px"> View Molecule List</button> 
        </form>
        <form action="element_list" enctype="multipart/form-data" method="post">
            <button type="submit" id="viewListButton"  style="font-size: 20px">View Element List</button> 
        </form>
    </body>
</html>
"""
alert = """<html>
    <div class="alert">incorrectly formatted file</div>
    <h2>Click back arrow to try again</h2>
</html>"""
element_list_helper = """ 
    <form action="home" enctype="multipart/form-data" method="post">
        <button type="submit" id="back" style="font-size: 30px">BACK HOME</button>
    </form>
    <h1>Add Element to List</h1>
    <form action="test" method="post">
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
    <form action="test2" method="post">
        <p>
            <label>Enter a Letter in List to Remove:<input id="removeCode" name="removeCode"/></label>
        </p>
        <button type ="submit" id="removeElementButton" name="removeElementButton">Remove Element</button>
    </form>
   
    <h2>Current Element List</h2>
"""
httpd = HTTPServer(('localhost', int(sys.argv[1])), Server);
print("opened server" + sys.argv[1] + "\n");
httpd.serve_forever();