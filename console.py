#!/usr/bin/python3

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '
    classes = ["BaseModel", "City", "State",
               "User", "Place", "Review", "Amenity"]

    def do_create(self, args):
        """
        Creates a new instance of BaseModel, saves it to JSON file
        and prints the id
        """
        if not args:
            print("** class name missing **")
            return None
        tokens = args.split(" ")
        if tokens[0] in self.classes:
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
            if tokens[0] in self.classes:
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

        if tokens[0] in self.classes:
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
        instances = []
        tokens = args.split(" ")
        if len(tokens) < 1:
            for value in objects.name():
                instances.append(name.__str__())
            print(instances)
        elif (tokens[0] not in self.classes):
            print("** class doesn't exist **")
        else:
            for key, name in objects.items():
                if tokens[0] in key:
                    instances.append(name.__str__())
                else:
                    return
            print(instances)

    def do_update(self, args):
        """
        Update an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        """
        tokens = args.split()
        if len(tokens) < 1:
            print("** class name missing **")
        elif (tokens[0] not in self.classes):
            print("** class doesn't exist **")
        elif len(tokens) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            name = tokens[0] + "." + tokens[1]
            if (name not in objects):
                print("** no instance found **")
        if tokens[0] in self.classes:
            if len(tokens) < 2:
                print("** instance id missing **")
                return
            name = tokens[0] + "." + tokens[1]
            if name not in objects:
                print("** no instance found **")
            elif len(tokens) < 3:
                print("** attribute name missing **")
            elif len(tokens) < 4:
                print("** value missing **")
            else:
                setattr(objects[name], tokens[2], tokens[3])
                storage.save()

    def do_quit(self, args):
        """
        Quit command exits out of the command interpreter
        """
        return True

    def do_EOF(self, args):
        """
        EOF command exits out of the command interpreter
        """
        print()
        return True

    def emptyline(self):
        """
        Returns back to the prompt
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
