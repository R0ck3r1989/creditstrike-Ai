package com.creditstrike.ai

import android.app.Activity
import android.os.Bundle
import android.graphics.Typeface
import android.view.Gravity
import android.view.ViewGroup
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class MainActivity : Activity() {
    private lateinit var body: LinearLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showHome()
    }

    private fun base(title: String): LinearLayout {
        val scroll = ScrollView(this)
        body = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(40, 48, 40, 40)
        }
        scroll.addView(body)
        setContentView(scroll)
        addText(title, 28f, true)
        addText("Private credit investigation workspace", 14f, false)
        return body
    }

    private fun addText(text: String, size: Float, bold: Boolean) {
        body.addView(TextView(this).apply {
            this.text = text
            textSize = size
            if (bold) setTypeface(typeface, Typeface.BOLD)
            setPadding(0, 18, 0, 18)
        })
    }

    private fun addButton(label: String, action: () -> Unit) {
        body.addView(Button(this).apply {
            text = label
            setOnClickListener { action() }
            layoutParams = LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
            ).apply { topMargin = 12; bottomMargin = 12 }
        })
    }

    private fun showHome() {
        base("CreditStrike AI")
        addText("CASE COMMAND CENTER", 13f, true)
        addText("Track derogatory accounts, organize evidence, and plan the next lawful step.", 18f, false)
        addButton("Account investigations") { showInvestigations() }
        addButton("Research library") { showResearch() }
        addButton("Approval queue") { showApprovals() }
        addText("Prototype notice: do not enter sensitive account numbers or upload real credit reports in this build. Authentication and secure storage are not yet implemented.", 14f, false)
    }

    private fun showInvestigations() {
        base("Account investigations")
        addText("Each account should have a specific, evidence-backed issue. A negative entry alone is not proof of an error.", 16f, false)
        addText("Suggested review checklist", 20f, true)
        listOf(
            "Confirm the account belongs to you",
            "Compare bureau, balance, dates, and status",
            "Check for duplicates or obsolete reporting",
            "Record the exact disputed field and supporting evidence",
            "Track correspondence and response dates",
            "Choose the next action only after reviewing the evidence"
        ).forEach { addText("•  $it", 16f, false) }
        addButton("Back to dashboard") { showHome() }
    }

    private fun showResearch() {
        base("Research library")
        addText("Planned source hierarchy", 20f, true)
        listOf(
            "Federal statutes and regulations",
            "CFPB and FTC official guidance",
            "Federal and state court opinions",
            "Florida statutes and regulator guidance",
            "Bureau and furnisher dispute procedures",
            "Secondary sources: books, videos, forums, commentary"
        ).forEach { addText("•  $it", 16f, false) }
        addText("The production research agent must attach citations, jurisdiction, dates, and verification status to legal conclusions.", 15f, false)
        addButton("Back to dashboard") { showHome() }
    }

    private fun showApprovals() {
        base("Approval queue")
        addText("No external action can be sent from this prototype.", 18f, true)
        addText("Production approval cards will show the proposed recipient, factual basis, supporting evidence, legal citations, expected effect, and deadline before you approve.", 16f, false)
        addButton("Back to dashboard") { showHome() }
    }
}
