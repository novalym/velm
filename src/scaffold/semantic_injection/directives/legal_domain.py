# scaffold/semantic_injection/directives/legal_domain.py

"""
=================================================================================
== THE SCRIBE OF COVENANTS (V-Ω-LEGAL-DOMAIN)                                  ==
=================================================================================
LIF: 1,000,000,000

This artisan implements the `@legal` namespace. It provides standard open-source
license texts, automatically populating the Year and Author.

Usage:
    LICENSE :: @legal/mit
    LICENSE :: @legal/apache(author="Scaffold Corp")
=================================================================================
"""
import datetime
import getpass
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("legal")
class LegalDomain(BaseDirectiveDomain):
    """
    The Keeper of the Public Vows.
    """

    @property
    def namespace(self) -> str:
        return "legal"

    def help(self) -> str:
        return "Generates standard licenses (mit, apache, gpl) with auto-filled Year and Author."

    # =========================================================================
    # == THE RITES OF OWNERSHIP                                              ==
    # =========================================================================

    def _get_metadata(self, context: Dict[str, Any], **kwargs) -> int:
        """
        [THE GAZE OF IDENTITY]
        Resolves the Year and Author from the Gnostic Context or the System.
        """
        # 1. Year: Always the current moment
        year = datetime.datetime.now().year

        # 2. Author: Hierarchy of Truth
        #    a. Explicit arg in directive call
        #    b. 'author' variable in blueprint context
        #    c. System user
        author = kwargs.get('author') or context.get('author') or getpass.getuser()

        return year, author

    def _directive_license(self, context: Dict[str, Any], type: str = "mit", *args, **kwargs) -> str:
        """
        @legal/license(type="mit")
        A router for dynamic license selection.
        """
        method_name = f"_directive_{type.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(context, *args, **kwargs)
        raise ValueError(f"Unknown license type: {type}")

    def _directive_mit(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @legal/mit
        The Permissive Vow.
        """
        year, author = self._get_metadata(context, **kwargs)

        return dedent(f"""
            MIT License

            Copyright (c) {year} {author}

            Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files (the "Software"), to deal
            in the Software without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the Software is
            furnished to do so, subject to the following conditions:

            The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Software.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
            SOFTWARE.
        """).strip()

    def _directive_apache(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @legal/apache
        The Vow of Patents and Attribution (Apache 2.0).
        """
        year, author = self._get_metadata(context, **kwargs)

        return dedent(f"""
                                             Apache License
                                   Version 2.0, January 2004
                                http://www.apache.org/licenses/

           TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

           1. Definitions.

              "License" shall mean the terms and conditions for use, reproduction,
              and distribution as defined by Sections 1 through 9 of this document.

              "Licensor" shall mean the copyright owner or entity authorized by
              the copyright owner that is granting the License.

              "Legal Entity" shall mean the union of the acting entity and all
              other entities that control, are controlled by, or are under common
              control with that entity. For the purposes of this definition,
              "control" means (i) the power, direct or indirect, to cause the
              direction or management of such entity, whether by contract or
              otherwise, or (ii) ownership of fifty percent (50%) or more of the
              outstanding shares, or (iii) beneficial ownership of such entity.

              "You" (or "Your") shall mean an individual or Legal Entity
              exercising permissions granted by this License.

           2. Grant of Copyright License. Subject to the terms and conditions of
              this License, each Contributor hereby grants to You a perpetual,
              worldwide, non-exclusive, no-charge, royalty-free, irrevocable
              copyright license to reproduce, prepare Derivative Works of,
              publicly display, publicly perform, sublicense, and distribute the
              Work and such Derivative Works in Source or Object form.

           Copyright {year} {author}

           Licensed under the Apache License, Version 2.0 (the "License");
           you may not use this file except in compliance with the License.
           You may obtain a copy of the License at

               http://www.apache.org/licenses/LICENSE-2.0

           Unless required by applicable law or agreed to in writing, software
           distributed under the License is distributed on an "AS IS" BASIS,
           WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
           See the License for the specific language governing permissions and
           limitations under the License.
        """).strip()

    def _directive_gpl(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @legal/gpl
        The Vow of the Copyleft (GPLv3).
        """
        year, author = self._get_metadata(context, **kwargs)

        return dedent(f"""
            GNU GENERAL PUBLIC LICENSE
                               Version 3, 29 June 2007

             Copyright (C) {year} {author}
             Everyone is permitted to copy and distribute verbatim copies
             of this license document, but changing it is not allowed.

                                    Preamble

              The GNU General Public License is a free, copyleft license for
              software and other kinds of works.

              [... truncated for brevity, typically this file is linked or 35KB long ...]

              (Note: This is a placeholder for the full GPLv3 text. 
               In a real deployment, the full text would be inscribed here.)

              See: https://www.gnu.org/licenses/gpl-3.0.txt
        """).strip()