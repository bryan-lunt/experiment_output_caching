import sys
import os
import hashlib

class MyHash(object):
    md5_prog_map = { ("posix","darwin"):"md5",
                    ("posix","linux2"):"md5sum",

    }
    def __init__(self,cache_dir,use_hash="md5"):
        self.os_name = os.name
        self.sys_platform = sys.platform
        #inputs shall be listed as tuples (TYPE, value)
        #the TYPE may be "file" or "bytes".
        #numerical values shall be converted to bytes, one way or another. A string works.
        #You can use this to enforce some rounding. (But should be careful!)
        self.inputs = list()
        self.outputs = list() #only file paths
        self.my_hash = use_hash
        self.cache_dir = cache_dir
        self.my_digest = None

    def add_file_input(self,filename):
        inputs.append(("file",filename))
        self.my_digest = None

    def add_bytes_input(self,the_bytes):
        inputs.append(("bytes",the_bytes))

    def hash_inputs(self,blocksize=2**12):
        the_hash = hashlib.new(self.my_hash)
        for i_type, i_value in self.inputs:
            if i_type == "bytes":
                the_hash.update(i_value)
                continue
            #implicit else:
            with open(i_value) as infile:
                while True:
                    partial = infile.read(blocksize)
                    if not partial:
                        break
                    the_hash.update(partial)
            #end of file case
        #end of all inputs
        fin_result = the_hash.hexdigest()
        self.my_digest = fin_result
        return fin_result

    def get_path(self):
        the_digest = self.my_digest if not (None is self.my_digest) else self.hash_inputs()
        return os.path.join(self.cache_dir,the_digest)

    def check_exists(self):
        """ This should be atomic..."""
        #TODO: make atomic.
        exists = os.path.exists(self.get_path())
        return exists

    def create(self):
        #TODO: make atomic.
        the_path = self.get_path()
        exists = self.check_exists()

    def move_in(self,source_file,dest_file=None):
        """ does not yet handle directory structure """
        dest_name = dest_file if not (None is dest_file) else os.path.basename(source_file)
        shutil.copy(source_file,os.path.join(self.get_path(),dest_name))

    def copy_out(self,dest_file,source_file=None):
        source_name = source_file if not (None is source_file) else os.path.basename(dest_file)
        shutil.copy(os.path.join(self.get_path(),source_name),dest_file)
