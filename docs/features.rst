Feature Matrix
==============

.. Sphinx and current RTD theme doesn't provide a way to create a table in the needed format, that
   is why we are using the raw html with redefined theme stylesheet here.

Architect is actively developed and new features are constantly added to it. Below is the current
feature status matrix of the Architect’s latest development version which can be found on GitHub.

.. raw:: html

    <table class="feature-matrix">
        <tr>
            <th class="invisible-cell" colspan="2"></th>
            <th class="orm">Django</th>
            <th class="orm">Peewee</th>
            <th class="orm">Pony</th>
            <th class="orm">SQLAlchemy</th>
        </tr>
        <tr>
            <td class="feature" colspan="6">Table partitioning</td>
        </tr>
        <tr>
            <td class="database" rowspan="2">PostgreSQL</td>
            <td class="subfeature">Range</td>
            <td class="implemented">YES</td>
            <td class="implemented">YES</td>
            <td class="implemented">YES</td>
            <td class="implemented">YES</td>
        </tr>
        <tr>
            <td class="subfeature">List</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
        </tr>
        <tr>
            <td class="database" rowspan="5">MySQL</td>
            <td class="subfeature">Range</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
        </tr>
        <tr>
            <td class="subfeature">List</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
        </tr>
        <tr>
            <td class="subfeature">Hash</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
        </tr>
        <tr>
            <td class="subfeature">Key</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
        </tr>
        <tr>
            <td class="subfeature">Composite</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
            <td class="not-implemented">NO</td>
        </tr>
    </table>
