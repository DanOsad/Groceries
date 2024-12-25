from extensions import db

class Grex_mon(db.Model):
    id                   = db.Column(db.Integer,     primary_key=True)
    tb                   = db.Column(db.Text,        default = None)
    bc                   = db.Column(db.Text,        default = None)
    srl                  = db.Column(db.Text,        default = None)
    user                 = db.Column(db.Text,        default = None)
    args                 = db.Column(db.Text,        default = None)
    data                 = db.Column(db.Text,        default = None)
    dump                 = db.Column(db.Text,        default = None)
    ports                = db.Column(db.Integer,     default = None)
    r_time               = db.Column(db.Integer,     default = None)
    c_time               = db.Column(db.DateTime,    default = None)
    q_time               = db.Column(db.DateTime,    default = None)
    s_time               = db.Column(db.DateTime,    default = None)
    e_time               = db.Column(db.DateTime,    default = None)
    h_name               = db.Column(db.String(255), default = None)
    job_id               = db.Column(db.Text,        default = 0)
    status               = db.Column(db.Text,        default = None)
    errors               = db.Column(db.Integer,     default = None)
    sv_cmd               = db.Column(db.Text,        default=None)
    passed               = db.Column(db.Integer,     default = None)
    failed               = db.Column(db.Integer,     default = None)
    crashed              = db.Column(db.Integer,     default = None)
    project              = db.Column(db.Text,        default = None)
    maxvmem              = db.Column(db.Text,        default = None)
    req_mem              = db.Column(db.Text,        default = None)
    timeout              = db.Column(db.Integer,     default = None)
    recheck              = db.Column(db.Text,        default=None)
    test_id              = db.Column(db.Text,        default = None)
    avg_mem              = db.Column(db.Integer,     default = None)
    mem_diff             = db.Column(db.Text,        default = None)
    uniq_jid             = db.Column(db.Text,        default = None)
    full_req             = db.Column(db.Text,        default = None)
    end_time             = db.Column(db.Text,        default = None)
    trex_log             = db.Column(db.Text,        default=None)
    tool_ver             = db.Column(db.Text,        default=None)
    is_alive             = db.Column(db.Boolean,     default=False)
    high_mem             = db.Column(db.Integer,     default = None)
    parent_id            = db.Column(db.String(255), default = None)
    test_name            = db.Column(db.String(255), default = None)
    r_time_ns            = db.Column(db.Integer,     default = None)
    port_type            = db.Column(db.Text,        default = None)
    is_parent            = db.Column(db.Boolean,     default=False)
    is_jenkins           = db.Column(db.Boolean,     default=False)
    start_time           = db.Column(db.Text,        default = None)
    error_type           = db.Column(db.Text,        default = None)
    gb_per_sec           = db.Column(db.Integer,     default = None)
    total_bytes          = db.Column(db.Integer,     default = None)
    sendToReRun          = db.Column(db.Integer,     default = None)
    sim_time_ns          = db.Column(db.Integer,     default = None)
    sim_rate_hz          = db.Column(db.Float,       default = None)
    run_time_sec         = db.Column(db.Integer,     default = None)
    instructions         = db.Column(db.Text,        default = None)
    total_cycles         = db.Column(db.Integer,     default = None)
    allow_to_run         = db.Column(db.Integer,     default = None)
    grid_crashed         = db.Column(db.Integer,     default = None)
    is_multi_inst        = db.Column(db.Boolean,     default=False)
    test_location        = db.Column(db.Text,        default = None)
    regression_name      = db.Column(db.Text,        default = None)
    last_alive_ping      = db.Column(db.DateTime,    default = None)
    trans_per_second     = db.Column(db.Integer,     default = None)
    total_transactions   = db.Column(db.Integer,     default = None)
    mem_usage_diff_float = db.Column(db.Float,       default = None)

    @property
    def as_dict(self):
        return { column.name: getattr(self, column.name) for column in self.__table__.columns }

    @property
    def serialize(self):
        return { attr: getattr(self, attr) for attr in self.columns }
    
    @property
    def columns(self):
        return [ column.name for column in self.__table__.columns ]