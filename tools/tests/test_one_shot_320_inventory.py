import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

script = Path(__file__).resolve().parents[1] / 'one_shot_320_inventory.py'
spec = importlib.util.spec_from_file_location('oneshot', script)
oneshot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oneshot)


def nid(name):
    return {'sceTest': 'ABCDEFGHIJK', 'sceNext': 'LMNOPQRSTUV', 'sceOther': '1234567890A'}.get(name, 'NO-MATCH-NI')


class InventoryTests(unittest.TestCase):
    def test_exact_source_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'libSceTest.c').write_text('''
            if(sprx_dlsym(__handle, "ABCDEFGHIJK", &__ptr_sceTest)) return;
            if(sprx_dlsym(__handle, "LMNOPQRSTUV", &__ptr_sceNext)) return;
            ''', encoding='utf-8')
            records, counts, files = oneshot.read_inventory(root, nid)
            self.assertEqual(len(records), 2)
            self.assertEqual(files, 1)
            self.assertTrue(records[('libSceTest', 'ABCDEFGHIJK')]['name_verified'])
            self.assertEqual(counts['observations'], 2)

    def test_parse_fails_closed_on_unsupported_syntax(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'libSceTest.c').write_text('sprx_dlsym(__handle, "ABCDEFGHIJK", &ptr);')
            with self.assertRaises(ValueError):
                oneshot.read_inventory(root, nid)

    def test_pr_scanning_picks_up_added_exports(self):
        class API:
            def open_pr_files(self):
                yield 25, [{'filename':'core/libs/prx/libSceTest/Export.cpp', 'status':'modified', 'changes':2,
                            'patch':'@@ -1,1 +1,3 @@\n+int APS5_VABI sceTest(void) {\n+}\n'}]
                yield 26, [{'filename':'core/libs/prx/libSceTest/Export2.cpp', 'patch':None}]
                yield 27, [{'filename':'core/libs/prx/libOther/Export.cpp', 'patch':None}]
        claimed, uncertain, scanned = oneshot.pending_exports(API(), nid, {'libSceTest'})
        self.assertEqual(scanned, 3)
        self.assertEqual(claimed[('libSceTest', 'ABCDEFGHIJK')], {25})
        self.assertEqual(uncertain['libSceTest'], {26})
        self.assertNotIn('libOther', uncertain)

    def test_report_makes_batches_without_source_mutations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entries = {('libSceTest', 'ABCDEFGHIJK'):{'module':'libSceTest', 'nid':'ABCDEFGHIJK', 'name':'sceTest', 'source':'libSceTest.c', 'name_verified':True},
                       ('libSceTest', 'LMNOPQRSTUV'):{'module':'libSceTest', 'nid':'LMNOPQRSTUV', 'name':'sceNext', 'source':'libSceTest.c', 'name_verified':True}}
            result = oneshot.write_report(root / 'result', entries, {'observations':2,'duplicates':0}, 1,
                          {'ABCDEFGHIJK':{'libSceTest'}}, set(), {'libSceTest'}, {}, {}, 0, 0, 150, 'head','source')
            self.assertEqual(result['status_counts']['already_present'], 1)
            self.assertEqual(result['status_counts']['candidate'], 1)
            self.assertEqual((root/'result/batches/libSceTest-001.nids').read_text(), 'LMNOPQRSTUV\n')
            self.assertEqual(json.loads((root/'result/summary.json').read_text())['candidate_batches'], 1)

    def test_uncertain_pr_blocks_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entry={('libSceTest','ABCDEFGHIJK'):{'module':'libSceTest','nid':'ABCDEFGHIJK','name':'sceTest','source':'libSceTest.c','name_verified':True}}
            result=oneshot.write_report(root/'out',entry,{'observations':1,'duplicates':0},1,{},set(),{'libSceTest'},{}, {'libSceTest': {123}},1,10,150,'x','y')
            self.assertEqual(result['status_counts'], {'needs_review':1})
            self.assertFalse((root/'out/batches').exists())


if __name__=='__main__':
    unittest.main()
