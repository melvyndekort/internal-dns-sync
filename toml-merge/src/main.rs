use std::fs;
use toml_edit::DocumentMut;

fn main() {
    let pihole = fs::read_to_string("/etc/pihole/pihole.toml")
        .expect("Failed to read pihole.toml");
    let dns_config = fs::read_to_string("/var/lib/internal-dns/dns-config.toml")
        .expect("Failed to read dns-config.toml");
    
    let mut pihole_doc = pihole.parse::<DocumentMut>()
        .expect("Failed to parse pihole.toml");
    let dns_doc = dns_config.parse::<DocumentMut>()
        .expect("Failed to parse dns-config.toml");
    
    // Replace hosts and cnameRecords while preserving comments and formatting
    pihole_doc["dns"]["hosts"] = dns_doc["dns"]["hosts"].clone();
    pihole_doc["dns"]["cnameRecords"] = dns_doc["dns"]["cnameRecords"].clone();
    
    fs::write("/etc/pihole/pihole.toml", pihole_doc.to_string())
        .expect("Failed to write pihole.toml");
    
    println!("DNS entries updated - comments and formatting preserved");
}
