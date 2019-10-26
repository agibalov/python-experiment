.. _dummy:

The Dummy Page
==============

Hello world *italic* **bold** ``monospace``.

Preformatted::

  aaa
    bbb
      ccc

Some PlantUML mind map diagram
------------------------------

.. uml::
  :align: center

  @startmindmap
  + OS
  ++ Ubuntu
  +++ Linux Mint
  +++ Kubuntu
  +++ Lubuntu
  +++ KDE Neon
  ++ LMDE
  ++ SolydXK
  ++ SteamOS
  ++ Raspbian
  -- Windows 95
  -- Windows 98
  -- Windows NT
  --- Windows 8
  --- Windows 10
  @endmindmap

Some PlantUML sequence diagram
------------------------------

.. uml::
  :align: center

  title "Messages - Sequence Diagram"

  actor User
  boundary "Web GUI" as GUI
  control "Shopping Cart" as SC
  entity Widget
  database Widgets

  User -> GUI : To boundary
  GUI -> SC : To control
  SC -> Widget : To entity
  Widget -> Widgets : To database

Some Python example
-------------------

.. code-block:: python

  def add(a: int, b: int) -> int:
    return a + b

Some Java example
-----------------

.. code-block:: java

  class App {
    static void main(string[] args) {
      System.out.printf("hello world!\n");
    }
  }

End.
