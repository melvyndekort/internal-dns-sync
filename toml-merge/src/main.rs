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

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    #[test]
    fn test_merge_preserves_other_settings() {
        let pihole_toml = r#"
[dns]
  port = 53
  localise = true
  
  hosts = [
    "10.0.0.1 old.example.com",
  ]
  
  cnameRecords = [
    "old.example.com,target.example.com",
  ]
  
  revServers = []
"#;

        let dns_config = r#"
[dns]
  hosts = [
    "10.0.0.2 new.example.com",
  ]
  
  cnameRecords = [
    "new.example.com,target.example.com",
  ]
"#;

        let mut pihole_doc = pihole_toml.parse::<DocumentMut>().unwrap();
        let dns_doc = dns_config.parse::<DocumentMut>().unwrap();

        pihole_doc["dns"]["hosts"] = dns_doc["dns"]["hosts"].clone();
        pihole_doc["dns"]["cnameRecords"] = dns_doc["dns"]["cnameRecords"].clone();

        let result = pihole_doc.to_string();

        // Check that hosts and cnameRecords were updated
        assert!(result.contains("new.example.com"));
        assert!(!result.contains("old.example.com"));

        // Check that other settings were preserved
        assert!(result.contains("port = 53"));
        assert!(result.contains("localise = true"));
        assert!(result.contains("revServers = []"));
    }

    #[test]
    fn test_merge_preserves_comments() {
        let pihole_toml = r#"
[dns]
  # This is an important comment
  port = 53
  
  # Custom DNS entries
  hosts = [
    "10.0.0.1 old.example.com",
  ]
"#;

        let dns_config = r#"
[dns]
  hosts = [
    "10.0.0.2 new.example.com",
  ]
"#;

        let mut pihole_doc = pihole_toml.parse::<DocumentMut>().unwrap();
        let dns_doc = dns_config.parse::<DocumentMut>().unwrap();

        pihole_doc["dns"]["hosts"] = dns_doc["dns"]["hosts"].clone();

        let result = pihole_doc.to_string();

        // Check that comments were preserved
        assert!(result.contains("# This is an important comment"));
        assert!(result.contains("# Custom DNS entries"));
    }

    #[test]
    fn test_handles_empty_arrays() {
        let pihole_toml = r#"
[dns]
  hosts = []
  cnameRecords = []
"#;

        let dns_config = r#"
[dns]
  hosts = [
    "10.0.0.1 test.example.com",
  ]
  cnameRecords = []
"#;

        let mut pihole_doc = pihole_toml.parse::<DocumentMut>().unwrap();
        let dns_doc = dns_config.parse::<DocumentMut>().unwrap();

        pihole_doc["dns"]["hosts"] = dns_doc["dns"]["hosts"].clone();
        pihole_doc["dns"]["cnameRecords"] = dns_doc["dns"]["cnameRecords"].clone();

        let result = pihole_doc.to_string();

        assert!(result.contains("test.example.com"));
    }
}
