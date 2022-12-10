from moonleap import Tpls, chop0

button_handler_tpl = chop0(
    """
    const {{ handler }} = () => {
        console.log("Moonleap Todo");
    };

"""
)

button_div_tpl = chop0(
    """
    <div
      className={cn("{{ class_name }}", "button")}
      onClick={ {{ handler }} }
    >
      {{ title }}
    </div>
"""
)

tpls = Tpls(
    "button_builder",
    button_div_tpl=button_div_tpl,
    button_handler_tpl=button_handler_tpl,
)
