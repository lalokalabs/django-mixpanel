from customerio import CustomerIO as OrigCustomerIO
from customerio import Regions

class CustomerIO(OrigCustomerIO):
    def track(self, *args, **kwargs):
        pass
    
    def identify(self, **kwargs):
        pass
