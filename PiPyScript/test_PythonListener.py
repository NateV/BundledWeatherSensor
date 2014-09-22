import unittest
import PythonListener

class TestPythonListener(unittest.Testcase):
  
  def test_findSerial(self):
    self.assertEquals(PythonListener.findSerial(), "/dev/tty.usbmodem1411")






if __name__ == '__main__':
  unittest.main()
