import dns.resolver
from termcolor import colored


def check_dmarc_policy(domain):
    try:
        # Query the DMARC record
        answers = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        for record in answers:
            txt_record = str(record).strip('"')
            if "v=DMARC1" in txt_record:
                # Extract the policy value
                policy = None
                for part in txt_record.split(";"):
                    if part.strip().startswith("p="):
                        policy = part.split("=")[1].strip()
                        break
                if policy:
                    return policy
    except Exception as e:
        print(colored(f"Error checking DMARC for {domain}: {e}", "red"))
        return None
    return None


def check_spf_record(domain):
    try:
        # Query the SPF record (TXT type can include SPF data)
        answers = dns.resolver.resolve(domain, "TXT")
        for record in answers:
            txt_record = str(record).strip('"')
            if "v=spf1" in txt_record:
                return txt_record
    except Exception as e:
        print(colored(f"Error checking SPF for {domain}: {e}", "red"))
        return None
    return None


def main(domains):
    results = {}

    for domain in domains:
        dmarc_policy = check_dmarc_policy(domain)
        spf_record = check_spf_record(domain)

        results[domain] = {"DMARC": dmarc_policy, "SPF": spf_record}

    # Print report with colors
    print(colored("\n==== DMARC and SPF Check Report ====\n", "cyan", attrs=["bold"]))

    for domain, records in results.items():
        dmarc_policy = records["DMARC"]
        spf_record = records["SPF"]

        # Display DMARC Policy
        if dmarc_policy:
            print(
                colored(f"{domain}: ", "yellow")
                + colored(f"DMARC Policy = {dmarc_policy}", "green")
            )
        else:
            print(
                colored(f"{domain}: ", "yellow")
                + colored("No DMARC Policy found", "red")
            )

        # Display SPF Record
        if spf_record:
            print(colored(f"    SPF Record = {spf_record}", "green"))
        else:
            print(colored(f"    No SPF Record found", "red"))

        print("-" * 50)


if __name__ == "__main__":
    domains = [
        "byu.edu",
        "tesla.com",
        "nasa.gov",
        "api.wisdomtreeprimeapp.com",
        "sokos.fi",
        "digili.s-cloud.fi",
        "s-ryhma.fi",
    ]
    main(domains)
