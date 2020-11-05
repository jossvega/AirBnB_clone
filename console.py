#!/usr/bin/python3

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = ["BaseModel", "City", "State", "User", "Place", "Review", "Amenity"]


class HBNBCommand(cmd.Cmd):

    prompt = '(hbnb) '

    def do_create(self, args):
        """
        Creates a new instance of BaseModel, saves it to JSON file
        and prints the id
        """
        if not args:
            print("** class name missing **")
            return None
        tokens = args.split(" ")
        if tokens[0] in classes:
            new = eval("{}()".format(tokens[0]))
            new.save()
            print("{}".format(new.id))
        else:
            print("** class doesn't exist **")
            return None

    def do_show(self, args):
        """ show string representation of an instance"""
        tokens = args.split()
        objects = storage.all()
        try:
            if len(tokens) == 0:
                print("** class name missing **")
                return None
            if tokens[0] in classes:
                if len(tokens) > 1:
                    key = tokens[0] + "." + tokens[1]
                    if key in objects:
                        obj = objects[key]
                        print(obj)
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        except AttributeError:
            print("** instance id missing **")

    def do_destroy(self, args):
        """
        Deletes an instance based on the class name and id
        saves the changes into JSON file
        """
        if not args:
            print("** class name missing **")
            return None
        tokens = args.split(" ")
        objects = storage.all()

        if tokens[0] in classes:
            if len(tokens) < 2:
                print("** instance id missing **")
                return None
            name = tokens[0] + "." + tokens[1]
            if name not in objects:
                print("** no instance found **")
            else:
                obj = objects[name]
                if obj:
                    objs = storage.all()
                    del objs["{}.{}".format(type(obj).__name__, obj.id)]
                    storage.save()
        else:
            print("** class doesn't exist **")
            return None

    def do_all(self, args):
        """
        Prints all string representation of all instances
        based or not on the class name
        """
        objects = storage.all()
        tokens = args.split(" ")
        if not args:
            instances = [str(obj) for key, obj in objects.items()]
            print(instances)
        elif (tokens[0] not in classes):
            print("{}".format("** class doesn't exist **"))
        else:
            instances = [str(obj) for key, obj in objects.items()
                         if type(obj).__name__ == tokens[0]]
            print(instances)

    def do_update(self, args):
        """
        Update an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        """
        objects = storage.all()
        tokens = args.split()
        if len(tokens) == 0:
            print("{}".format("** class name missing **"))
        elif tokens[0] not in self.dict_classes:
            print("{}".format("** class doesn't exist **"))
        elif len(tokens) == 1:
            print("{}".format("** instance id missing **"))
        # key = "{}.{}".format(tokens[0], tokens[1])
        elif ".".join(tokens[:2]) not in objects:
            print("{}".format("** no instance found **"))
        elif len(tokens) == 2:
            print("{}".format("** atribute name missing **"))
        elif len(tokens) < 4:
            print("{}".format("** value missing **"))
        else:
            key = "{}.{}".format(tokens[0], tokens[1])
            attribute = tokens[2]
            value = tokens[3].strip(' "')
            if value.isdigit():
                value = int(value)
            elif '.' in value:
                float1 = value.split('.')
                if float1[0].isdigit() and float1[1].isdigit():
                    value = float(value)
            dic_obj = objects[key].__dict__
            dic_obj[attribute] = value
            storage.save()

    def do_count(self, args):
        """
        Counts number of instances of a class
        """
        objects = storage.all()
        instances = []
        count = 0
        if args in self.classes:
            for name in objects:
                if name[0:len(args)] == args:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def do_quit(self, args):
        """
        Quit command exits out of the command interpreter
        """
        return True

    def do_EOF(self, args):
        """
        EOF command exits out of the command interpreter
        """
        return True

    def emptyline(self):
        """
        Returns back to the prompt
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
