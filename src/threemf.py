"""Write the stand out as a 3MF project: one file, parts kept apart, colours set.

STL cannot do this.  An STL file is a bare list of triangles with no notion
of colour, material, or even where one body ends and the next begins, so a
two-colour model has to travel as two STLs and be lined up again at the
other end.  3MF is the format that fixes exactly that, and every slicer
worth using reads it.

The parts are written as *components of a single object* rather than as
separate objects side by side.  That matters: as separate objects a slicer
is free to move them independently, and one auto-arrange would slide the
mark off the plate it belongs to.  As components they move together and
cannot come apart.

Colours are carried twice over.  ``<basematerials>`` is the core 3MF way and
is what a generic slicer reads; ``Metadata/model_settings.config`` is the
Bambu Studio and Orca convention, where each part names the filament slot it
wants (1-based).  A slicer that understands neither still gets the geometry
and the parts, and assigning two filaments by hand is a couple of clicks.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
"""


def _mesh_xml(mesh) -> str:
    """A <mesh> element.  Built by joining strings -- these run to tens of
    thousands of triangles and an XML DOM for that is needlessly slow."""
    v = np.asarray(mesh.vertices, float)
    f = np.asarray(mesh.faces, int)
    verts = "".join(
        '<vertex x="%.5f" y="%.5f" z="%.5f"/>' % tuple(p) for p in v
    )
    tris = "".join(
        '<triangle v1="%d" v2="%d" v3="%d"/>' % tuple(t) for t in f
    )
    return f"<mesh><vertices>{verts}</vertices><triangles>{tris}</triangles></mesh>"


def write(path: Path, parts: list[tuple[str, object, str, int]], title: str) -> None:
    """Write a 3MF holding ``parts``.

    Each part is ``(name, mesh, "#RRGGBB", filament_slot)``, and the slot is
    1-based to match what Bambu Studio and Orca expect.
    """
    bases = "".join(
        '<base name="%s" displaycolor="%sFF"/>' % (name, colour)
        for name, _, colour, _ in parts
    )

    objects, components, config_parts = [], [], []
    for i, (name, mesh, _, slot) in enumerate(parts):
        oid = i + 2                     # 1 is the basematerials group
        objects.append(
            f'<object id="{oid}" name="{name}" type="model" pid="1" pindex="{i}">'
            f"{_mesh_xml(mesh)}</object>"
        )
        components.append(f'<component objectid="{oid}"/>')
        config_parts.append(
            f'  <part id="{oid}" subtype="normal_part">\n'
            f'   <metadata key="name" value="{name}"/>\n'
            f'   <metadata key="extruder" value="{slot}"/>\n'
            f"  </part>"
        )

    root_id = len(parts) + 2
    model = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US"'
        ' xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
        f'<metadata name="Title">{title}</metadata>'
        '<metadata name="Application">MMFT-STL</metadata>'
        "<resources>"
        f'<basematerials id="1">{bases}</basematerials>'
        + "".join(objects)
        + f'<object id="{root_id}" name="{title}" type="model">'
        f"<components>{''.join(components)}</components></object>"
        "</resources>"
        f'<build><item objectid="{root_id}"/></build>'
        "</model>\n"
    )

    settings = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<config>\n"
        f' <object id="{root_id}">\n'
        f'  <metadata key="name" value="{title}"/>\n'
        + "\n".join(config_parts)
        + "\n </object>\n</config>\n"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for name, data in (
            ("[Content_Types].xml", CONTENT_TYPES),
            ("_rels/.rels", RELS),
            ("3D/3dmodel.model", model),
            ("Metadata/model_settings.config", settings),
        ):
            # A zip stamps every entry with the time it was written, so the
            # same model would otherwise produce a different file on every
            # build and show up as changed in git.  Pin the timestamp.
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
