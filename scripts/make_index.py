import os
import sys

import jinja2

this_dir = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    template_fn = os.path.join(this_dir, '..', 'static', 'index.template')
    with open(template_fn, 'r') as f:
        template = jinja2.Template(f.read())
    output = template.render()
    output_fn = os.path.join(this_dir, '..', 'static', 'index.html')
    with open(output_fn, 'w') as of:
        of.write(output)
