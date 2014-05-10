'''

ref: http://stackoverflow.com/questions/1173992/what-is-a-basic-example-of-single-inheritance-using-the-super-keyword-in-pytho

'''


class Foo(object):
     def __init__(self, frob, frotz):
          self.frobnicate = frob
          self.frotz = frotz

class Bar(Foo):
     def __init__(self, frob, frizzle):

          Foo.__init__(self, frob, frizzle)   # Gives 1 and 2 to Foo's frob and frotz, but frotz is overwritten by the next line...
          self.frotz = 34                     # Writes over Foo's frotz with Bar's frotz literal.
          self.frazzle = frizzle              


bar = Bar(1,2)
print("bar.frobnicate:", bar.frobnicate)
print("bar.frotz:", bar.frotz)                # Shows Bar is using its literal instead of what it got from its Foo components. If it was not set to 34, it would have been 2.
print("bar.frazzle:", bar.frazzle)


krk = input("\n\nPress enter to end program . . .")