from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import EthAddr

log = core.getLogger()

# MAC addresses
H1_MAC = EthAddr("00:00:00:00:00:01")
H2_MAC = EthAddr("00:00:00:00:00:02")

def _handle_ConnectionUp(event):
    log.info("Switch connected. Installing firewall rules...")

    # 🚫 BLOCK h1 -> h2 (by source MAC = h1)
    msg = of.ofp_flow_mod()
    msg.priority = 100
    msg.idle_timeout = 0   # Never expire
    msg.hard_timeout = 0   # Never expire
    msg.match.dl_src = H1_MAC
    msg.match.dl_dst = H2_MAC
    # No actions = DROP
    event.connection.send(msg)
    log.info("Installed DROP rule: h1 -> h2")

    # 🚫 BLOCK h2 -> h1 (optional: block reverse too)
    msg2 = of.ofp_flow_mod()
    msg2.priority = 100
    msg2.idle_timeout = 0
    msg2.hard_timeout = 0
    msg2.match.dl_src = H2_MAC
    msg2.match.dl_dst = H1_MAC
    event.connection.send(msg2)
    log.info("Installed DROP rule: h2 -> h1")

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    src_mac = packet.src
    dst_mac = packet.dst

    # 🚫 Explicitly drop h1 <-> h2 at controller level too (safety net)
    blocked_pairs = [
        (H1_MAC, H2_MAC),
        (H2_MAC, H1_MAC),
    ]
    if (src_mac, dst_mac) in blocked_pairs:
        log.info(f"Dropping packet from {src_mac} to {dst_mac}")
        return  # Do nothing = DROP

    # ✅ Allow and flood all other traffic
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.in_port = event.port
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    log.info("Firewall Controller Running")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
