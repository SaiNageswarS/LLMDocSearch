import unittest
import textwrap
from ChunkPdf import __get_clean_paragraphs__


class TestEmbedPdfs(unittest.TestCase):
    def test_get_clean_paragraphs(self):
        mock_content = """
            The mechanism by which camphor produces toxicity is

            unknown. Absorption from the gastrointestinal tract occurs
            rapidly with detectable serum concentrations found within
            minutes after ingestion (6,7). Within 5–15 minutes, patients
            commonly complain of mucus membrane irritation, nausea,
            vomiting, and abdominal pain. Generalized tonic-clonic
            convulsions are often the first sign of significant toxicity
            and can occur soon after ingestion (8–11). Central nervous
            system depression is commonly seen, as are headache, diz-
            ziness, confusion, agitation, anxiety, hallucinations, myo-
            clonus, and hyperreflexia (6,7,12–18). Death is usually the
            result of respiratory failure or convulsions (6,12,19,20).
            
            Even when applied to the skin in large quantities, camphor has
            only rarely been reported to cause systemic poisoning resembling
            the effects seen with acute ingestion exposures (11,21,22).
        """

        clean_paras = __get_clean_paragraphs__(textwrap.dedent(mock_content))
        self.assertEqual(len(clean_paras), 2)
