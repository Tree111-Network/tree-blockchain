from tree.types.blockchain_format.program import INFINITE_COST
from tree.types.spend_bundle import SpendBundle
from tree.types.generator_types import BlockGenerator
from tree.consensus.cost_calculator import NPCResult
from tree.consensus.default_constants import DEFAULT_CONSTANTS
from tree.full_node.bundle_tools import simple_solution_generator
from tree.full_node.mempool_check_conditions import get_name_puzzle_conditions


def cost_of_spend_bundle(spend_bundle: SpendBundle) -> int:
    program: BlockGenerator = simple_solution_generator(spend_bundle)
    npc_result: NPCResult = get_name_puzzle_conditions(
        program, INFINITE_COST, cost_per_byte=DEFAULT_CONSTANTS.COST_PER_BYTE, mempool_mode=True
    )
    return npc_result.cost
