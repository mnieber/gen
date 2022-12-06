from moonleap.utils import chop0

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
