
class DataTargetManagerFactory:
    @staticmethod
    def create_target_manager(target_type, **kwargs):
        if target_type == "sftp":
            return 
        else:
            raise ValueError(f"{target_type} is not supported")
