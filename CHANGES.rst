0.5.5 (05/09/2017):

- Django 1.11 compatibility (#5 by @jan-lugfl)

0.5.4 (29/09/2015):

- Triggered autodiscover in navutils, fix #1 failing example

0.5.3 (21/08/2015):

- Added microdata for better breadcrumb handling by search engines

0.5.2 (22/07/2015):

- Fixed context that wasn't passed from menu to node

0.5.1 (22/07/2015):

- Updated ``PassTestNode`` with context argument

0.5 (22/07/2015):

- ``Node.is_viewable_by`` now takes a ``context`` argument

0.4 (19/06/2015):

- ``Menu`` and ``Node`` now accept extra context

0.3 (03/06/2015):

- Added ``MenuMixin`` for handling current menu node

0.2 (24/05/2015):

- Added PermissionNode for checking against a single permission
- Added AllPermissionsNode for checking against all permissions in set of permission
- Added AnylPermissionsNode for checking against any permissions in set of permission
- Added PassTestNode for providing a custom check

0.1.4 (21/05/2015):

- removed useless print statement

0.1.3 (21/05/2015):

- added MANIFEST (templates were not included)

0.1.2 (21/05/2015):

- added MANIFEST (templates were not included)

0.1.1 (21/05/2015):

- Added changelog
- Fixed IndexError when building seo_title


0.1.0 (20/05/2015):

- initial release
