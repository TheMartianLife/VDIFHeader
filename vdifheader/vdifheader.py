class VDIFHeader:
    def __init__(self, file_path, show_debug=True):
        self.invalid_flag = 0
        self.legacy_mode = 0
        self.seconds_from_epoch = 0
        self._unassigned_field = 0
        self.reference_epoch = 0
        self.data_frame_number = 0
        self.vdif_version = 0
        self._log2_num_channels = 0
        self.num_channels = 0
        self.data_frame_length = 0
        self.data_type = 0
        self.bits_per_sample = 0
        self.thread_id = 0
        self.station_id = 0
        self.extended_data_version = 0

    def __repr__(self):
        repr_string = "<VDIFHeader"
        for field in self.__public_fields():
            repr_string += "\n"
            repr_string += repr(field)
        repr_string += ">"
        return repr_string

    def __str__(self):
        return f"<VDIFHeader station_id={self.station_id},\
            timestamp={self.get_timestamp()}>"

    def __public_fields(self):
        return [f for f in self.__dict__ if not f.startswith(' ')]

    def get_timestamp(self):
        '''Returns reference_epoch + seconds_from_epoch as datetime object'''
        return

    def print_summary(self):
        return

    def print_values(self):
        return

    def print_raw(self):
        return

    def print_verbose(self):
        self.print_raw()
        self.print_values()
        self.print_summary()
        return