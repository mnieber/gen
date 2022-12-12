from moonleap import Tpls, chop0

button_div_tpl = chop0(
    """
    <div
      className={cn("{{ class_name }}", "button")}
      onClick={() => {console.log("Moonleap Todo")}}
    >
      {{ title }}
    </div>
"""
)

tpls = Tpls(
    "button_builder",
    button_div_tpl=button_div_tpl,
)
